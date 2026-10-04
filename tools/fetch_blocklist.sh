#!/bin/bash
# Downloads the latest prebuilt blocklist (built daily by GitHub Actions) into the Content Blocker target.
# No Python or Swift needed. Rebuild the app in Xcode afterwards.
set -euo pipefail
cd "$(dirname "$0")"
OUT="../Safari Ad Blocker/Safari Ad Blocker Content Blocker/blockerList.json"
URL="https://github.com/biswadipb/SafariAdBlock/releases/download/blocklist-latest/blockerList.json"
curl -fL --retry 3 --progress-bar -o "$OUT.new" "$URL"
python3 -c 'import json,sys; n=len(json.load(open(sys.argv[1]))); assert n>1000, n; print(n, "rules")' "$OUT.new"
mv "$OUT.new" "$OUT"
echo "Updated $OUT"
