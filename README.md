# SHEMKAR | Application Security Research Portfolio

A lightweight, mobile-friendly, no-build static website created for the GitHub Pages user site of `bossyassine78-ship-it`.

## Contents

- `index.html`: homepage, research cards, project links, methodology
- `research/evidence-before-confidence.html`: original reflection on capturing reproducible evidence
- `labs/session-lifecycle.html`: fictional interactive JavaScript security state-machine exercise
- `assets/`: styles, script, favicon

**Safety and disclosure:** No private bug bounty submissions, real endpoint names, real tokens, cookies, raw proofs of concept, or screenshots are included. The research field note shares only general lessons; the interactive lab is explicitly fictional. Do not copy the uploaded report HTML or its assets into this public repo.

## Test locally

From this directory:

```sh
python3 -m http.server 8000
```

Visit http://localhost:8000 .

## Publish free with GitHub Pages

1. On GitHub, sign in as `bossyassine78-ship-it` and create a **public** repository named `bossyassine78-ship-it.github.io` (exactly).
2. Upload all files and folders **inside** this directory to the **root** of the new repository. (Do not upload the containing `shemkar-portfolio` folder itself.)
3. Open repository **Settings → Pages**. Under **Build and deployment**, choose **Deploy from a branch**, select **main** and **/(root)**, then Save.
4. Once GitHub confirms deployment, visit `https://bossyassine78-ship-it.github.io`.

Official docs: https://docs.github.com/en/pages/quickstart

## Before publishing

- Review the text for whether it sounds like you. Nothing is presented as a verified private vulnerability.
- Add a public LinkedIn URL or an email contact only after choosing what you want made public.
- Add more work only after confirming its disclosure permissions.
- Keep research claims tied to verified evidence. Avoid implying a program patched a finding without confirmation.

## Editing

All text is plain HTML. Styles are in `assets/style.css`. The small navigation and interactive lab code are in `assets/app.js`. No framework or npm required.