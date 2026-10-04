#!/usr/bin/env python3
"""Convert Adblock Plus filter lists (EasyList) into a Safari Content Blocker JSON list.

Usage: convert_easylist.py [-o blockerList.json] [URL_OR_FILE ...]
Defaults to EasyList, EasyPrivacy, Fanboy's Annoyance List and the EasyList Cookie List
"""
import argparse, json, re, sys, urllib.request
from collections import defaultdict

DEFAULT_LISTS = [
    "https://easylist.to/easylist/easylist.txt",
    "https://easylist.to/easylist/easyprivacy.txt",
    "https://easylist.to/easylist/fanboy-annoyance.txt",
    "https://secure.fanboy.co.nz/fanboy-cookiemonster.txt",
]
MAX_RULES = 149000  # Safari's limit is 150,000 per content blocker

TYPE_MAP = {
    "script": "script", "image": "image", "stylesheet": "style-sheet",
    "xmlhttprequest": "raw", "font": "font", "media": "media", "popup": "popup",
    "ping": "raw", "websocket": "raw", "other": "raw", "object": "media",
    "subdocument": "document", "document": "document",
}
ALL_TYPES = ["document", "image", "style-sheet", "script", "font", "raw", "media", "popup"]
IGNORED_OPTS = {"important", "match-case", "all"}
# Selector features Safari can't evaluate
BAD_SELECTOR = re.compile(r":-abp-|:has-text|:xpath|:matches-|:contains|:upward|:nth-ancestor|:remove|:style|:watch-attr|:min-text|:others|:not\(:|\\")

def fetch(src):
    if re.match(r"https?://", src):
        req = urllib.request.Request(src, headers={"User-Agent": "SafariAdBlock-converter"})
        return urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")
    return open(src, encoding="utf-8", errors="replace").read()

def pattern_to_regex(p):
    if not p:
        return ".*"
    if p.startswith("/") and p.endswith("/") and len(p) > 2:
        return None  # raw regexes aren't portable
    if "|" in p.strip("|") or not p.isascii():
        return None
    out = ""
    i = 0
    if p.startswith("||"):
        out, i = r"^[a-z]+://([^/]*\.)?", 2
    elif p.startswith("|"):
        out, i = "^", 1
    end = p.endswith("|") and not p.endswith("||")
    body = p[i:-1] if end else p[i:]
    for ch in body:
        if ch == "*": out += ".*"
        elif ch == "^": out += r"[/:?=&#]"
        elif ch in ".+?(){}[]\\$": out += "\\" + ch
        else: out += ch
    if end: out += "$"
    return out

def domains(spec):
    inc, exc = [], []
    for d in spec.split("|"):
        if not d or "*" in d or "/" in d or not d.isascii(): continue
        (exc if d.startswith("~") else inc).append("*" + d.lstrip("~"))
    return inc, exc

def parse_network(line, exception):
    pattern, opts = line, ""
    m = re.match(r"^(.*)\$([a-z0-9_\-~=|,.*/]*)$", line, re.I)
    if m and not line.startswith("/"):
        pattern, opts = m.group(1), m.group(2)
    trig_regex = pattern_to_regex(pattern)
    if trig_regex is None:
        return None
    trigger = {"url-filter": trig_regex}
    types, neg_types, inc, exc = [], [], [], []
    for o in filter(None, opts.split(",")):
        neg = o.startswith("~")
        name = o.lstrip("~").lower()
        if name == "third-party" or name == "3p":
            trigger["load-type"] = ["first-party"] if neg else ["third-party"]
        elif name == "first-party" or name == "1p":
            trigger["load-type"] = ["third-party"] if neg else ["first-party"]
        elif name.startswith("domain="):
            inc, exc = domains(name[7:])
            if not inc and not exc: return None
        elif name == "match-case":
            trigger["url-filter-is-case-sensitive"] = True
        elif name in IGNORED_OPTS:
            continue
        elif name in TYPE_MAP:
            (neg_types if neg else types).append(TYPE_MAP[name])
            if name == "subdocument" and not neg:
                trigger["load-context"] = ["child-frame"]
        else:
            return None  # csp, redirect, removeparam, etc.
    if exception and any(o.lstrip("~").lower() in ("document", "elemhide", "generichide", "genericblock") for o in filter(None, opts.split(","))):
        return None
    if types:
        trigger["resource-type"] = sorted(set(types))
    elif neg_types:
        trigger["resource-type"] = [t for t in ALL_TYPES if t not in neg_types and t != "popup"]
    if inc: trigger["if-domain"] = inc
    elif exc: trigger["unless-domain"] = exc
    return {"trigger": trigger,
            "action": {"type": "ignore-previous-rules" if exception else "block"}}

def convert(text, stats):
    block, exceptions = [], []
    generic_css = []
    domain_css = defaultdict(list)
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith(("!", "[")):
            continue
        if "#?#" in line or "#$#" in line or "#@#" in line or "##+js" in line or "#%#" in line:
            stats["skipped"] += 1; continue
        if "##" in line:
            doms, sel = line.split("##", 1)
            if not sel or BAD_SELECTOR.search(sel) or not sel.isascii():
                stats["skipped"] += 1; continue
            if not doms:
                generic_css.append(sel)
            else:
                inc, exc = domains(doms.replace(",", "|"))
                if exc or not inc:
                    stats["skipped"] += 1; continue
                for d in inc: domain_css[d].append(sel)
            continue
        if "#@#" in line or "#" in line and re.search(r"#[@?$%]*#", line):
            stats["skipped"] += 1; continue
        exception = line.startswith("@@")
        rule = parse_network(line[2:] if exception else line, exception)
        if rule is None:
            stats["skipped"] += 1; continue
        (exceptions if exception else block).append(rule)
    css_rules = []
    # Generic hiding, batched so each selector list stays a manageable size
    for i in range(0, len(generic_css), 500):
        css_rules.append({"trigger": {"url-filter": ".*"},
                          "action": {"type": "css-display-none",
                                     "selector": ", ".join(generic_css[i:i + 500])}})
    # Sites that share an identical selector list share one rule (saves thousands of rules).
    by_selectors = defaultdict(list)
    for d, sels in domain_css.items():
        by_selectors[", ".join(sorted(set(sels)))].append(d)
    for selector, doms in sorted(by_selectors.items()):
        for i in range(0, len(doms), 1000):
            css_rules.append({"trigger": {"url-filter": ".*", "if-domain": sorted(doms[i:i + 1000])},
                              "action": {"type": "css-display-none", "selector": selector}})
    return block, css_rules, exceptions

def dedupe(rules):
    seen, out = set(), []
    for r in rules:
        k = json.dumps(r, sort_keys=True)
        if k not in seen:
            seen.add(k); out.append(r)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", default="blockerList.json")
    ap.add_argument("--extra", help="JSON file of extra rules (e.g. hand-written) to prepend")
    ap.add_argument("lists", nargs="*", default=DEFAULT_LISTS)
    a = ap.parse_args()
    stats = defaultdict(int)
    block, css, exc = [], [], []
    if a.extra:
        block += json.load(open(a.extra))
    for src in a.lists:
        b, c, e = convert(fetch(src), stats)
        block += b; css += c; exc += e
    block, css, exc = dedupe(block), dedupe(css), dedupe(exc)
    # Order matters: blocks, then css, then exceptions that cancel earlier rules.
    budget = MAX_RULES - len(exc) - len(css)
    if len(block) > budget:
        print(f"warning: trimming {len(block) - budget} network rules to fit Safari's limit", file=sys.stderr)
        block = block[:budget]
    rules = block + css + exc
    json.dump(rules, open(a.output, "w"), separators=(",", ":"))
    print(f"network blocks: {len(block)}  css-hide: {len(css)}  exceptions: {len(exc)}  "
          f"total: {len(rules)}  skipped(unsupported): {stats['skipped']}")

if __name__ == "__main__":
    main()
