# Installing Safari Ad Blocker (macOS)

This builds the app from source in Xcode and turns on its two Safari extensions. It takes about 10 minutes.

**You need:** a Mac with Safari 16.4 or later, Xcode 14 or later (free on the Mac App Store), and an Apple ID (free).

## 1. Get the project and the blocklist

```bash
git clone https://github.com/biswadipb/SafariAdBlock.git ~/SafariAdBlock
```

```bash
cd ~/SafariAdBlock && ./tools/fetch_blocklist.sh
```

The blocklist (about 147,000 rules) is built daily by GitHub Actions and is not stored in git, so this download step is required. If you skip it, the build fails with a "blockerList.json is missing" error.

## 2. Open the project in Xcode

```bash
open ~/SafariAdBlock/"Safari Ad Blocker/Safari Ad Blocker.xcodeproj"
```

## 3. Choose a signing method

Xcode must sign the app and both extensions. There are three targets, and **each one needs the same settings**. Select a target in the left-hand TARGETS list, open its **Signing & Capabilities** tab, set it up, then repeat for the other two:

- **Safari Ad Blocker** (the app)
- **Safari Ad Blocker Extension** (popups, redirects, YouTube)
- **Safari Ad Blocker Content Blocker** (the filter lists)

Pick **one** of the two methods below.

### Method A: Sign to Run Locally (recommended, simplest)

This needs no Apple ID and no keychain access, so it avoids the keychain problems described in the troubleshooting section.

1. Untick **Automatically manage signing**.
2. Set **Team** to **None**, if Xcode allows it.
3. Set **Signing Certificate** to **Sign to Run Locally**.
4. Repeat for all three targets.

You must then turn on **Allow Unsigned Extensions** in Safari (step 5). Safari forgets this setting each time it quits, so you have to turn it on again after restarting Safari.

### Method B: Sign with your Apple ID

1. Tick **Automatically manage signing**.
2. Set **Team** to your name, ending in **(Personal Team)**. If no team is listed, choose **Add an Account...** and sign in with your Apple ID.
3. Change the **Bundle Identifier** so it is unique to you. Replace `example` with your own word, and keep the `.Extension` and `.ContentBlocker` endings:

   | Target | Bundle Identifier |
   |---|---|
   | Safari Ad Blocker | `com.yourname.safariadblock` |
   | Safari Ad Blocker Extension | `com.yourname.safariadblock.Extension` |
   | Safari Ad Blocker Content Blocker | `com.yourname.safariadblock.ContentBlocker` |

   Each extension's ID must **start with the app's ID**. The app contains the two extensions, and macOS refuses to load an extension whose ID does not begin with its parent app's ID.
4. Repeat for all three targets.

Xcode may ask for your Mac's **login keychain password** the first time it signs. This is normally your Mac login password. Click **Always Allow**, not **Allow**, or it asks again for every file. If it rejects the password, see Troubleshooting.

## 4. Build and run

1. At the top of Xcode, set the scheme to **Safari Ad Blocker** and the destination to **My Mac**.
2. Press **⌘R** (or the ▶ button).
3. A small app window opens. You can leave it open or close it.

## 5. Allow unsigned extensions (Method A only)

If you used Method A, or Safari does not list the extensions:

1. In Safari, open the **Develop** menu and choose **Allow Unsigned Extensions**. Enter your Mac password if asked.
2. If there is no Develop menu, go to **Safari → Settings → Advanced** and tick **Show features for web developers**.

This setting resets every time Safari quits.

## 6. Turn on both extensions in Safari

Open **Safari → Settings → Extensions** and tick both:

- **Safari Ad Blocker Content Blocker**: applies the filter lists. It needs no permissions.
- **Safari Ad Blocker Extension**: popup and redirect protection and YouTube ad skipping. Select it and set **Always Allow on Every Website** (or choose **Allow** when prompted). Without this, it does nothing.

## 7. Check that it works

Reload a news site and a YouTube video. If the Content Blocker shows an error in Safari's extension settings, see Troubleshooting.

## Updating the blocklist

The list is rebuilt every day. To get the newest one into your installed app:

```bash
cd ~/SafariAdBlock && ./tools/fetch_blocklist.sh
```

Then press **⌘R** in Xcode again. Safari reads the list only from inside the app, so the app cannot update itself; you must rebuild.

## Troubleshooting

### "codesign wants to access key ... in your keychain", and the password is not accepted

This happens when Method B is used and the login keychain password does not work in that dialog.

1. Check the keychain password is accepted. In Terminal, run the command below, then type your Mac login password at the prompt. Nothing appears as you type, which is normal:
   ```bash
   security unlock-keychain ~/Library/Keychains/login.keychain-db
   ```
   - If the prompt returns with no message, the password is correct and the keychain is unlocked.
   - If you get an error, the keychain password does not match your Mac login password.
2. Click **Deny** on the dialog, press **⌘.** to stop the build in Xcode, then quit Xcode with **⌘Q**.
3. Reopen the project (step 2) and press **⌘R**. When the dialog appears, enter the password and click **Always Allow**.
4. If the dialog still rejects the password, stop retrying and switch all three targets to **Method A (Sign to Run Locally)**.
5. As a last resort, open **Keychain Access → Settings → Reset My Default Keychains...**. This creates a new empty login keychain and **deletes passwords saved only in the old one**, so use it only if nothing else works.

### The extensions do not appear in Safari

- Make sure the app was built and run (step 4) at least once.
- If you used Method A, turn on **Develop → Allow Unsigned Extensions** (step 5). It resets when Safari quits.
- Quit Safari fully (⌘Q) and reopen it, then check **Safari → Settings → Extensions** again.

### The build fails with a signing or provisioning error

- Make sure all three targets use the same method and the same settings.
- With Method B, check each extension's Bundle Identifier starts with the app's.
- If it still fails, switch all three targets to Method A.

### The build fails because `blockerList.json` is missing

Run `./tools/fetch_blocklist.sh` (step 1), then build again.

### The Content Blocker shows an error in Safari

The list may be corrupt or over Safari's 150,000-rule limit. Run `./tools/fetch_blocklist.sh` again and rebuild. To build the list yourself, run `./tools/update_blocklist.sh`; it refuses to install a list that WebKit cannot compile.

### YouTube shows a dark screen and a spinner for as long as an ad would last

Something is blocking YouTube's own ad requests, so the player waits out the ad before playing the video. The project avoids this by not blocking YouTube's first-party requests (the exemption is `YOUTUBE_EXEMPTION` in `tools/convert_easylist.py`), and by removing the ads from the player data in the web extension instead.

1. Run `./tools/fetch_blocklist.sh` to get the latest list.
2. Rebuild with **⌘R** in Xcode.
3. Quit Safari fully (**⌘Q**), reopen it, turn **Allow Unsigned Extensions** back on if you use local signing, and reload YouTube.

If you added your own rules, make sure none block `youtube.com/api/stats/ads`, `/pagead`, `/ptracking` or `/get_midroll_`.

### A website is broken

Turn off the extensions for that site in **Safari → Settings → Websites** (use the Extensions and Content Blockers entries), then open an issue with the site's name.

### `gh: command not found` or `./tools/fetch_blocklist.sh: Permission denied`

`fetch_blocklist.sh` does not use `gh`; it only needs `curl`. If you get "Permission denied", run `chmod +x tools/*.sh` first.
