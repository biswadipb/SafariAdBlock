# SafariAdBlock

A Safari extension for macOS that blocks ads and trackers on all sites, stops intrusive popups and redirects, and skips YouTube ads.

## Features

- **EasyList filtering (Content Blocker):** ~135,000 rules converted from [EasyList](https://easylist.to) (ads), EasyPrivacy (trackers), Fanboy's Annoyance List (popups, social widgets) the EasyList Cookie List (cookie banners) and the URLhaus malware filter (known malware and phishing hosts) block ad, tracker and malicious requests and hide ads, cookie notices and other page clutter on every site. Runs inside Safari's native content-blocking engine, so it is fast and private.
- **Extra ad/tracker rules:** a hand-picked set of 85+ domains plus generic ad-container hiding (`extension/rules.json`, `extension/generic.css`).
- **Popup and redirect protection:** blocks popups and popunders without a click, off-site auto-redirects, click-hijacking overlays, and popunder networks.
- **YouTube:** strips ad data from the player and auto-skips any ad that still plays.

## Requirements

- macOS with Safari 16.4 or later
- Xcode 14 or later (free from the Mac App Store)

## Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/biswadipb/SafariAdBlock.git
   cd SafariAdBlock
   ```
2. **Open the project in Xcode**
   ```bash
   open "Safari Ad Blocker/Safari Ad Blocker.xcodeproj"
   ```
3. **Set up signing.** Click the project in the left sidebar. For **both** targets ("Safari Ad Blocker" and "Safari Ad Blocker Extension"), open **Signing & Capabilities** and either:
   - choose your **Team** (a free Apple ID works), and change the **Bundle Identifier** to something unique such as `com.yourname.safariadblock` (the extension's must start with the app's), or
   - set Signing Certificate to **Sign to Run Locally**.
4. **Build and run.** Choose the **Safari Ad Blocker** scheme with **My Mac** as the destination, then press **⌘R**. A small app window opens; you can leave it.
5. **Allow unsigned extensions** (only if you used "Sign to Run Locally" or Safari doesn't list the extension). In Safari, open **Develop → Allow Unsigned Extensions** and enter your password. If you don't see a Develop menu, enable it under **Safari → Settings → Advanced → Show features for web developers**. This setting resets every time Safari quits.
6. **Enable both extensions.** In Safari, open **Safari → Settings → Extensions** and tick:
   - **Safari Ad Blocker Content Blocker** (the EasyList rules)
   - **Safari Ad Blocker Extension** (popup/redirect protection and YouTube)
7. **Grant website access.** Select **Safari Ad Blocker Extension** and set **Always Allow on Every Website** (or choose **Allow** when prompted). Without this, popup protection and YouTube skipping will not work. The Content Blocker needs no permissions.
8. **Test it.** Reload any page, for example a YouTube video.

## Updating

**Refresh the filter lists** (they change daily; the malware list updates every 12 hours). This downloads the latest EasyList, EasyPrivacy, Fanboy's Annoyance List, EasyList Cookie List and URLhaus malware filter, converts it, checks it with WebKit's own rule compiler, and installs it:

```bash
./tools/update_blocklist.sh
```

Then rebuild with ⌘R. You need Python 3 and Xcode's command line tools. To use other lists, pass their URLs, for example `./tools/update_blocklist.sh https://easylist.to/easylist/easylist.txt https://easylist.to/easylist/easyprivacy.txt`. Passing URLs replaces the default set, so list every one you want. Safari allows at most 150,000 rules per Content Blocker, and the converter trims anything above that. The default set uses about 135,000. Sites that share identical hiding rules are merged to save space.

**Edit the web extension.** Change files in `extension/`. The Xcode project references them directly, so just rebuild with ⌘R.

## Troubleshooting

- **Content Blocker shows an error in Safari:** re-run `./tools/update_blocklist.sh`; it refuses to install a list that WebKit cannot compile.
- **Extension not in the list:** run the app from Xcode once and make sure the unsigned-extensions setting from step 5 is on.
- **A page is greyed out or won't scroll after a cookie banner disappears:** the cookie list hides the banner but doesn't accept or reject cookies. Disable the Content Blocker for that site under Safari → Settings → Websites → Content Blockers.
- **A site is broken:** disable the extension for that site under Safari → Settings → Websites → Extensions, and open an issue with the site name.
- **Ads still appear:** update EasyList (above) or open an issue with the site.

## Limitations

Safari's content blocker cannot run EasyList's advanced rules (scriptlets, `:has-text()` selectors, redirects and similar), so about 2,800 lines are skipped. It also cannot intercept a page changing its own address with `location.href`. Coverage is close to, but not the same as, uBlock Origin.
