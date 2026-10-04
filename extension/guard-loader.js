// Injects popup-guard.js into the page's own JS world.
{
  const s = document.createElement("script");
  s.src = (globalThis.browser || globalThis.chrome).runtime.getURL("popup-guard.js");
  s.onload = () => s.remove();
  (document.head || document.documentElement).appendChild(s);
}

// Remove invisible full-page overlays that hijack clicks to open ads.
function sweepOverlays() {
  const vw = innerWidth, vh = innerHeight;
  for (const el of document.body ? document.body.children : []) {
    const cs = getComputedStyle(el);
    if (cs.position !== "fixed" && cs.position !== "absolute") continue;
    const r = el.getBoundingClientRect();
    const covers = r.width >= vw * 0.9 && r.height >= vh * 0.9;
    const invisible = parseFloat(cs.opacity) < 0.05 || cs.backgroundColor === "rgba(0, 0, 0, 0)";
    const empty = !el.innerText.trim() && !el.querySelector("img,video,input,button,form");
    if (covers && invisible && empty && (parseInt(cs.zIndex) || 0) > 999) el.remove();
  }
}
setInterval(sweepOverlays, 1000);
