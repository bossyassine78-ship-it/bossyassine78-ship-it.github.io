# SHEMKAR — Portfolio (PRIVATE DRAFT)

This repository is a **work-in-progress website**, not a bug bounty report repository. Please review the website before any public launch.

**Current state:** GitHub repository set to Private. Work on this branch (`draft/portfolio-review`) is NOT a GitHub Pages release. Do not merge or publish until the owner approves.

## What is here?

- `index.html`: the homepage with research topics and projects.
- `research/evidence-before-confidence.html`: a personal article about evidence and reproducibility. It does not disclose a private report.
- `research/oauth-recovery-chain.html`, `research/mfa-state-boundary.html`, `research/function-level-authorization.html`, `research/graphql-alt-entrypoint.html`: original analysis of **other researchers' already-public** HackerOne/Bugcrowd write-ups. Each article links to the original author/source. These are NOT Shemkar's own reported bugs.
- `labs/session-lifecycle.html`: an independently built fictional interactive learning demo.
- `assets/style.css`: the site's visual style.
- `assets/app.js`: mobile menu and lab interactivity.
- `README.md`: this explanation for the repository owner, NOT a page or security report shown as a featured article.

## How to PREVIEW privately (no hosting)

1. While logged into GitHub, open this private repository.
2. Click **Code → Download ZIP**.
3. Extract the ZIP somewhere on your computer.
4. Open `index.html` in a browser. The CSS, scripts, pages and fictional lab use relative paths and should work offline.

Optional local server (from the extracted folder):

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## Important distinctions

- **Private repository** = only authorized GitHub accounts can read its source.
- **Public research** in the articles = original reports that other researchers have already published. It does **not** mean the portfolio should be public now.
- **GitHub Pages** is a separate website deployment. A private repository alone is not a promise that a Pages website is private; review Pages settings before sharing or launching.

No private Bugcrowd reports, HTTP requests, target names, real PoC captures, tokens or cookies have been intentionally added to this site. Review all words and links before publishing.

## Release checklist (not approved yet)

- [ ] Owner reviews every page and approves positioning.
- [ ] Owner approves which credited public-research analyses to keep.
- [ ] Visual/browser QA on mobile and desktop.
- [ ] Ensure no private vulnerability disclosure.
- [ ] Explicit owner approval before publishing website or merging draft changes to `main`.
