# SafariAdBlock

A Safari extension for macOS that blocks ads and trackers on all sites, stops intrusive popups and redirects, and skips YouTube ads.

## Features

- **Ad and tracker blocking:** network rules for 85+ major ad and tracker domains (`extension/rules.json`).
- **Ad hiding:** hides common ad containers on every site (`extension/generic.css`).
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
6. **Enable the extension.** In Safari, open **Safari → Settings → Extensions**, tick **Safari Ad Blocker Extension**.
7. **Grant website access.** With the extension selected, set **Always Allow on Every Website** (or choose **Allow** when prompted). Without this, blocking will not work.
8. **Test it.** Reload any page, for example a YouTube video.

## Updating

Edit files in `extension/`, then regenerate the Xcode project:

```bash
xcrun safari-web-extension-converter extension \
  --project-location . --app-name "Safari Ad Blocker" \
  --bundle-identifier com.yourname.safariadblock --macos-only --no-open --force
```

Rebuild with ⌘R. The `Safari Ad Blocker/` folder contains a copy of the extension files, so don't edit them there.

## Troubleshooting

- **Extension not in the list:** run the app from Xcode once and make sure the unsigned-extensions setting from step 5 is on.
- **A site is broken:** disable the extension for that site under Safari → Settings → Websites → Extensions, and open an issue with the site name.
- **Ads still appear:** ad networks change often, and the domain list is short. Open an issue with the site.

## Limitations

This is not a full filter-list blocker like uBlock Origin. It cannot intercept a page changing its own address with `location.href`, and ads served from unlisted or first-party domains can get through.
