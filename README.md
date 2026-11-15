# SHEMKAR

**Application Security Research · Security Testing · Systems Programming**

I investigate identity, authorization and session lifecycle boundaries. My focus is reproducible observations, clear test prerequisites, and practical fixes.

**Portfolio:** https://bossyassine78-ship-it.github.io/

## Featured work

| Project | Demonstrates | Status |
| --- | --- | --- |
| [Original authorization lab](labs/authz-lab/) | Local HTTP API with BOLA, role authorization and deleted-account state flaws. Vulnerable/fixed behavior and Python regression tests. | Original runnable lab |
| [Technical assessment](research/sample-api-assessment.html) | Full synthetic assessment with HTTP evidence, root causes, remediation and retest. | Published lab document |
| [Some of my losses. One of my wins.](research/some-of-my-losses-one-win.html) | Personal learning from research, reproduction, review and evidence limits. | Disclosure-safe field notes |
| [Session-state demonstration](labs/session-lifecycle.html) | Client-side simulation of token-only versus account-state-aware checks. | Interactive lab |
| [printf_checker](https://github.com/bossyassine78-ship-it/printf_checker) | C printf test automation. | Public |
| [libft](https://github.com/bossyassine78-ship-it/libft) | C standard-library fundamentals and linked lists. | Public |
| ft_printf | Variadic formatted output in C. | WIP, private source |

## Research workflow

1. Define the expected security invariant and trust boundary.
2. Model the smallest reproducible hypothesis.
3. Preserve exact request, response, state, assumptions and timing.
4. Separate demonstrated impact from speculative exploitation.
5. Verify the result after remediation.

## Run

Website: static HTML, CSS and JavaScript. No build step.

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

From the repository root, open http://127.0.0.1:8000.

API lab:

```sh
cd labs/authz-lab
python3 -m unittest -v test_lab.py
```

## Layout

- `index.html` homepage
- `assets/` presentation and interactions
- `research/` writing and synthetic case studies
- `labs/` local exercises and reproducible source

## Disclosure

Real-world security research is published only with permission under applicable program rules. The public portfolio does not reproduce confidential submissions, report IDs, actual target endpoints, credentials, victim data or undisclosed exploit details. Synthetic examples are explicitly labeled.

*Evidence before confidence.*
