#!/bin/bash
# Downloads the latest EasyList, converts it, validates it with WebKit, and installs it
# into the Content Blocker target. Rebuild the app in Xcode afterwards.
set -euo pipefail
cd "$(dirname "$0")"
OUT="../Safari Ad Blocker/Safari Ad Blocker Content Blocker/blockerList.json"
python3 convert_easylist.py -o "$OUT.new" "$@"
swiftc -O validate.swift -o /tmp/sab-validate
/tmp/sab-validate "$OUT.new"
mv "$OUT.new" "$OUT"
echo "Updated $OUT"
