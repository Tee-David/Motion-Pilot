# Security Policy

## Supported versions

Security fixes are applied to the latest release.

## Reporting a vulnerability

Please do not disclose exploitable vulnerabilities in a public issue. Use GitHub's private vulnerability reporting when it is enabled for this repository; otherwise contact the maintainer privately through the contact method on their GitHub profile.

## What Motion Pilot runs

The skill's scripts run locally on your machine:

- `brand_probe.py` opens the URL you give it in a headless browser and saves screenshots and page text.
- `render.py` opens local HTML project files in a headless browser.
- `fetch_font.py` downloads open-licence fonts from the Google Fonts repository.
- `voice_elevenlabs.py` calls the ElevenLabs API only when you run it with your key.

Review a project's HTML and JavaScript before rendering it if you did not write it, as you would any web page you open.

## Secrets

The only secret the skill reads is `ELEVENLABS_API_KEY`, from your environment. Never paste keys into a conversation, a project file, a script or an issue. Generated projects never store keys.

## Client material

Brand files, unreleased screens and voice recordings you give the skill stay in your project folder. Keep them out of public repositories and issues.
