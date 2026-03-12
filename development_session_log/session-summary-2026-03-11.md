# ConsentWise Development Session Summary
**Date:** 11 March 2026
**Duration:** Full day session
**Repo:** texashedgeem/consentwise

---

## What We Built Today

### SDLC Foundation (CWPD-5 — Done)

| # | Ticket | Delivered |
|---|--------|-----------|
| 1 | CWPD-15 | Pre-commit hook — enforces `TYPE(CWPD-NNN): description` on every commit |
| 2 | CWPD-14 | Playwright functional test framework — 10 tests, runs against Jekyll on port 4001 |
| 3 | CWPD-17 | Auto GitHub Release notes on push to main — semver auto-increment, Jira links |
| 4 | CWPD-16 | GitHub Actions CI — Playwright runs on every PR, uploads report on failure |
| — | — | Branch protection on `main` — require 1 approval, dismiss stale, block force push |
| — | — | Second GitHub account (`simonhewinszodia`) for PR approvals (self-approval not permitted) |
| — | — | `enforce_admins: true` — admins can no longer bypass CI/review requirements |
| — | — | Required status checks — CI must pass before any PR can merge |

### SDLC Documentation (CWPD-6)

| # | Ticket | Delivered |
|---|--------|-----------|
| 5 | CWPD-18 | `CONTRIBUTING.md` — local setup, branching, commit format, testing, PR process |
| 6 | CWPD-19 | `SDLC.md` — ISO 27001:2022, SOC 1, and DORA control mapping |

### Video Gallery Feature (CWPD-1 Initiative)

| # | Ticket | Delivered |
|---|--------|-----------|
| 7 | CWPD-7 | `_videos` Jekyll collection registered in `_config.yml`, front matter schema defined |
| 8 | CWPD-8 | `_layouts/video.html` — title hero, responsive YouTube embed, description, tags, CTA |
| 9 | CWPD-9 | 8 videos pre-populated (1 live, 7 with `youtube_id: TBD` for Simon to fill in) |
| 10 | CWPD-10 | Video tile grid added to `/promo-videos/` page — YouTube thumbnails + Coming Soon placeholders |
| 11 | CWPD-11 | Video tile styling — `aspect-ratio: 16/9`, `object-fit: cover`, consistent with services page |
| 12 | CWPD-12 | Full-width YouTube embed (covered in CWPD-8 layout) |
| 13 | CWPD-13 | CTA footer on video pages (covered in CWPD-8 layout) |
| 14 | CWPD-27 | Responsive video tile grid — 3 col desktop, 2 col tablet, 1 col mobile; 2-line title cap |

### Infrastructure / Release

| # | What | Detail |
|---|------|--------|
| 15 | `package-lock.json` committed | Was never tracked — caused all CI runs to fail silently |
| 16 | Release workflow updated | Added `feat!` / `fix!` major version bump support |
| 17 | Commit-msg hook updated | Now allows `!` breaking change marker |
| 18 | Jira version 1.0.0 created | fixVersion set on all CWPD tickets for this release |
| 19 | PR #13 open | `feat!(CWPD-1)` trigger commit — will create GitHub Release v1.0.0 on merge |

### Housekeeping

- CWPD-20 to CWPD-24: Low-priority initiative captured for CSS/SCSS migration (parked)
- CWPD-25: Definition of Done story created (backlog)
- CWPD-26: Phase 2 Playwright tests story created (backlog)
- Jira API auth fixed — must use Base64 `Authorization: Basic` header (not curl `-u` flag)
- `JIRA_TOKEN` added to `~/.zshrc` permanently

---

## Things Simon Needs To Do

### Before Next Session (Manual Review Required)

- [ ] **Check all Jira tickets** — Many are still in Backlog/In Progress. Review content via Jira UI before closing. Tickets to close: CWPD-1, 2, 3, 4, 6, 11, 18, 19, 27
- [ ] **Review GitHub Release notes** — Check releases at https://github.com/texashedgeem/consentwise/releases. Several auto-generated releases exist (v0.1.0 through v0.7.2). Consider whether to tidy these up or leave as audit trail
- [ ] **Check the live site** — https://consentwise.io/promo-videos/ — review video tile grid and individual video page in production
- [ ] **Approve and merge PR #13** — https://github.com/texashedgeem/consentwise/pull/13 — wait for CI to go green first (it must pass now that `enforce_admins: true`). Approve via `simonhewinszodia` account
- [ ] **Fill in YouTube video IDs** — 7 videos have `youtube_id: TBD` in `_videos/`. Update these in a future session

---

## Session Two Plan

### Immediate (complete the release)

1. **Merge PR #13** — CI should pass (package-lock.json now committed). Creates GitHub Release v1.0.0
2. **Close Jira tickets** — Once PR #13 is merged and production is verified: close CWPD-1, 2, 3, 4, 6, 11, 18, 19, 27 and mark Jira version 1.0.0 as Released
3. **Tidy GitHub Releases** — Consider editing v0.1.0–v0.7.2 to note they were pre-release development tags, and v1.0.0 as the first official release

### Short Term (backlog priority order)

4. **CWPD-25** — Add Definition of Done to CONTRIBUTING.md and SDLC.md
5. **CWPD-26** — Write Phase 2 Playwright tests for video tile grid, individual video pages, responsive breakpoints
6. **YouTube video IDs** — Fill in the 7 TBD videos in `_videos/`

### Strategic: Release Branch Deployment Strategy

**Current problem:** Every merge to `main` auto-deploys to production (GitHub Pages). This means individual feature merges go live immediately — there is no staging gate, no release branch, no product owner sign-off before production deployment.

**What you want:** Code accumulates on a development integration branch. Only when a release is ready — all features tested, PO sign-off, QA complete — does it deploy to production.

**Proposed approach:**

```
feature/CWPD-NNN  →  develop  →  (PO sign-off)  →  main (production)
```

- `develop` = integration branch, not deployed
- `main` = production, protected, only updated via a formal release PR
- GitHub Pages deploys from `main` only
- Release PR from `develop` → `main` requires:
  - CI green
  - PO approval (via `simonhewinszodia` account)
  - Optional: GitHub Actions environment approval gate (manual approval step in workflow)

**To implement this:**
- Rename current `main` to `develop` (or create `develop` from main)
- Protect both branches
- Update CI workflow to run on both `develop` PRs and release PRs
- Update release workflow to only fire on merges to `main`
- Update CONTRIBUTING.md and SDLC.md
- Update GitHub Pages source to deploy from `main`

This is a meaningful change to the entire SDLC flow — recommend a dedicated initiative (CWPD-2x) with its own epics and stories.

---

## Current Ticket Status

| Ticket | Type | Status | Notes |
|--------|------|--------|-------|
| CWPD-1 | Initiative | Backlog | Close after PR #13 merged and verified |
| CWPD-2 | Epic | Backlog | Close after PR #13 merged |
| CWPD-3 | Epic | Backlog | Close after PR #13 merged |
| CWPD-4 | Epic | Backlog | Close after PR #13 merged |
| CWPD-5 | Epic | Done | ✅ |
| CWPD-6 | Epic | Backlog | Close after PR #13 merged |
| CWPD-7–13 | Story | Done | ✅ |
| CWPD-14–17 | Story | Done | ✅ |
| CWPD-18 | Story | In Progress | Close after PR #13 merged |
| CWPD-19 | Story | In Progress | Close after PR #13 merged |
| CWPD-20–24 | Initiative/Epic/Story | Backlog | Low priority CSS migration — parked |
| CWPD-25 | Story | Backlog | Definition of Done — Session 2 |
| CWPD-26 | Story | Backlog | Phase 2 Playwright tests — Session 2 |
| CWPD-27 | Story | Backlog | Close after PR #13 merged |

---

## Technical Notes

- **Local dev:** `bundle exec jekyll serve --port 4001` (port 4000 often in use)
- **Kill port:** `lsof -ti :4000 | xargs kill -9` or `pkill -f jekyll`
- **Run tests:** `npm test` (Jekyll must be running on port 4001)
- **Jira API:** Must use `Authorization: Basic <base64(email:token)>` header — curl `-u` flag is unreliable in this shell
- **GitHub approver:** `simonhewinszodia` — second account for PR approvals
- **CI status check name:** `Run Playwright functional tests`
- **Release trigger:** `feat!(CWPD-NNN):` in commit message triggers major version bump
