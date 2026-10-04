# SafariAdBlock

A Safari extension for macOS that blocks ads and trackers on all sites, stops intrusive popups and redirects, and skips YouTube ads.

## Features

- **EasyList filtering (Content Blocker):** ~147,500 rules converted from [EasyList](https://easylist.to) (ads), EasyPrivacy (trackers), Fanboy's Annoyance List (popups, social widgets) the EasyList Cookie List (cookie banners) and the URLhaus malware filter (known malware and phishing hosts) EasyList Adult (ads on adult sites), NoCoin (in-browser crypto miners) and Dandelion Sprout's Anti-Malware List (malware and scam sites) block ad, tracker and malicious requests and hide ads, cookie notices and other page clutter on every site. Runs inside Safari's native content-blocking engine, so it is fast and private.
- **Extra ad/tracker rules:** a hand-picked set of 85+ domains plus generic ad-container hiding (`extension/rules.json`, `extension/generic.css`).
- **Popup and redirect protection:** blocks popups and popunders without a click, off-site auto-redirects, click-hijacking overlays, and popunder networks.
- **YouTube:** strips ad data from the player and auto-skips any ad that still plays.

## Requirements

- macOS with Safari 16.4 or later
- Xcode 14 or later (free from the Mac App Store)

## Installation

**See [INSTALL.md](INSTALL.md) for the full step-by-step guide**, including the two ways to sign the app and fixes for common keychain and signing problems.

Quick version:

1. Clone the repo and download the blocklist:
   ```bash
   git clone https://github.com/biswadipb/SafariAdBlock.git ~/SafariAdBlock
   cd ~/SafariAdBlock && ./tools/fetch_blocklist.sh
   ```
2. Open `Safari Ad Blocker/Safari Ad Blocker.xcodeproj` in Xcode.
3. For **all three targets**, open **Signing & Capabilities** and either set **Signing Certificate** to **Sign to Run Locally** (untick automatic signing), or choose your **Team** and give each target a unique Bundle Identifier.
4. Press **⌘R** with the **Safari Ad Blocker** scheme and **My Mac** selected.
5. In Safari, turn on **Develop → Allow Unsigned Extensions** (only needed for local signing; it resets when Safari quits).
6. In **Safari → Settings → Extensions**, enable both extensions, and set **Safari Ad Blocker Extension** to **Always Allow on Every Website**.

## Updating

**The blocklist updates itself in the repo.** A GitHub Action (`.github/workflows/update-blocklist.yml`) runs daily, downloads the latest filter lists, converts and validates them, and publishes the result to a single rolling release called `blocklist-latest`. Because it replaces one release file instead of committing a new 18 MB file each time, the repo does not grow.

To get the newest list into your installed app, download it and rebuild with ⌘R:

```bash
./tools/fetch_blocklist.sh
```

Safari reads the list only from inside the app, so the app cannot update itself; you must rebuild to pick up a new list.

**Build the list yourself** instead (needs Python 3 and Xcode's command line tools). This downloads the filter lists directly, converts them, and checks them with WebKit's own rule compiler:

```bash
./tools/update_blocklist.sh
```

To use other lists, pass their URLs, for example `./tools/update_blocklist.sh https://easylist.to/easylist/easylist.txt https://easylist.to/easylist/easyprivacy.txt`. Passing URLs replaces the default set, so list every one you want. Safari allows at most 150,000 rules per Content Blocker, and the converter trims anything above 149,000. The default set uses about 147,500. Sites that share identical hiding rules are merged to save space.

**Edit the web extension.** Change files in `extension/`. The Xcode project references them directly, so just rebuild with ⌘R.

## Troubleshooting

See also the troubleshooting section of [INSTALL.md](INSTALL.md).

- **Build fails because `blockerList.json` is missing:** run `./tools/fetch_blocklist.sh` first. The list is not stored in git.
- **Content Blocker shows an error in Safari:** re-run `./tools/update_blocklist.sh`; it refuses to install a list that WebKit cannot compile.
- **Extension not in the list:** run the app from Xcode once and make sure the unsigned-extensions setting from step 5 is on.
- **A page is greyed out or won't scroll after a cookie banner disappears:** the cookie list hides the banner but doesn't accept or reject cookies. Disable the Content Blocker for that site under Safari → Settings → Websites → Content Blockers.
- **A site is broken:** disable the extension for that site under Safari → Settings → Websites → Extensions, and open an issue with the site name.
- **Ads still appear:** update EasyList (above) or open an issue with the site.

## Limitations

Safari's content blocker cannot run EasyList's advanced rules (scriptlets, `:has-text()` selectors, redirects and similar), so about 4,100 lines are skipped. It also cannot intercept a page changing its own address with `location.href`. Coverage is close to, but not the same as, uBlock Origin.
