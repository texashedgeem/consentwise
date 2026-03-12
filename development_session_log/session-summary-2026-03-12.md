# ConsentWise Development Session Summary
**Date:** 12 March 2026
**Duration:** Full day session
**Repo:** texashedgeem/consentwise
**Session:** 2 of ongoing development

---

## Context

Session 2 picked up from the Session 1 plan. PR #13 had already been merged overnight and GitHub Release v1.0.0 had been automatically created. The session focused on completing the video library, improving the site UX, and strengthening the CI/CD pipeline.

---

## What We Built Today

### Video Library — YouTube IDs (CWPD-28)

| # | File | YouTube ID | Notes |
|---|------|------------|-------|
| 1 | `open-banking-explained.md` | `3PtGXB0eofc` | Existing file updated |
| 2 | `strong-customer-authentication.md` | `kJfTz-jypEU` | Existing file updated |
| 3 | `tpp-registration-open-banking-directory.md` | `rypDMxN9uuM` | Existing file updated |
| 4 | `future-of-open-banking-uk.md` | `Q4iuzeS5dKg` | Existing file, starts at 525s |
| 5 | `uk-open-banking-api-standards.md` | `YMYShcUJPz0` | Existing file updated |
| 6 | `variable-recurring-payments.md` | `-8PwbtE0h7g` | New file created |
| 7 | `oauth-consent-flows-open-banking.md` | `ZV5yTm4pT8g` | New file created |
| 8 | `account-information-services.md` | `pJ5jvpZD3dg` | Split from AIS vs PIS |
| 9 | `payment-initiation-services.md` | `jLFjz0e-fiM` | Split from AIS vs PIS |
| — | `account-information-vs-payment-initiation.md` | — | Deleted — replaced by two separate files above |

**Remaining TBD:** `open-banking-testing-best-practices.md` (CWPD-32)

### Open Banking Video Curriculum (CWPD-28 / CWPD-29)

Developed a 20-video Open Banking Mastery curriculum covering 7 stages:
- Stage 1: Foundations — Stage 2: Regulation — Stage 3: Architecture
- Stage 4: TPPs — Stage 5: Developer Implementation — Stage 6: Advanced — Stage 7: Future

CWPD-29 created to track sourcing the remaining ~13 videos. Full curriculum stored as a comment on CWPD-29 in Jira.

### Video UX Improvements

| # | Ticket | Change |
|---|--------|--------|
| 1 | CWPD-30 | Added `rel=0` to YouTube embed URL — suppresses random end-screen recommendations |
| 2 | CWPD-31 | Reduced video hero title from `6rem` to `3rem` — scoped to `.video-hero h1` only |

### Learn Page (CWPD-33 / CWPD-34)

Created a standalone `/learn/` page as the Open Banking educational video library, separate from the Promo Videos service page:

| Page | URL | Purpose |
|------|-----|---------|
| Learn | `/learn/` | Free educational video library for users to build Open Banking domain knowledge |
| Promo Videos | `/promo-videos/` | Commercial service — ConsentWise produces promotional videos for clients |

- Added **Learn** nav item to top navigation (primary menu and burger menu) between About Us and Services
- Both pages currently share `site.videos` collection — will diverge as CWPD-29 progresses
- **Bug found and fixed:** Learn nav initially pointed to `/services/promo-videos/` (404) — corrected to `/promo-videos/` then updated to `/learn/` after the page was created

### Navigation Playwright Tests (CWPD-33)

Added `tests/e2e/pages/navigation.spec.js` covering:
- About Us, Learn, and Services nav items all link to correct URLs
- Learn appears between About Us and Services (order assertion)
- These tests would have caught the `/services/promo-videos/` 404 bug immediately

### CI Audit Trail (CWPD-35)

Significant improvement to the CI/CD pipeline:

| Before | After |
|--------|-------|
| Triggered on PRs to `main` only | Triggers on every push to every branch |
| Report uploaded on failure only | Report always uploaded |
| `list` reporter only | `list` + `html` + **JUnit XML** reporters |
| 7-day artifact retention | 30-day artifact retention |
| No step summary | GitHub Actions step summary with pass/fail counts per run |
| Artifact name: `playwright-report` | Artifact name: `playwright-report-<commit-sha>` |

Each commit now produces a permanent, linked test evidence record satisfying SDLC audit requirements (ISO27001/SOC1/DORA).

### New Jira Tickets Created This Session

| Ticket | Summary |
|--------|---------|
| CWPD-28 | Add YouTube IDs to Open Banking video library — initial 10 videos |
| CWPD-29 | Expand Open Banking video library to 20-video curriculum |
| CWPD-30 | Suppress related video recommendations on YouTube embeds |
| CWPD-31 | Reduce video page title font size by 50% |
| CWPD-32 | Source YouTube video for Open Banking Testing Best Practices |
| CWPD-33 | Add Learn nav item to top navigation between About Us and Services |
| CWPD-34 | Create standalone Learn page as the Open Banking educational video library |
| CWPD-35 | Implement Playwright CI audit trail — test report on every commit |

### PR and Release

- **PR #14** merged to `main` — https://github.com/texashedgeem/consentwise/pull/14
- Confirmed working in production at https://consentwise.io
- Test suite: **14 tests passing** (up from 10 at start of session)

---

## Things Simon Needs To Do

### Immediate

- [ ] **Close Jira tickets from Session 1** — CWPD-1, 2, 3, 4, 6, 18, 19, 27 (all unblocked now PR #13 merged)
- [ ] **Mark Jira version 1.0.0 as Released**
- [ ] **Close Jira tickets from Session 2** — CWPD-28, 30, 31, 33, 34, 35 (all delivered and in production)
- [ ] **Find YouTube video for CWPD-32** — Open Banking Testing Best Practices. Suggested search: `"open banking" testing sandbox API "best practices" fintech developer 2023 OR 2024`

### Backlog

- [ ] **CWPD-29** — Source remaining ~13 videos from the 20-video curriculum (paste YouTube URLs, I'll create the files)
- [ ] **CWPD-25** — Add Definition of Done to `CONTRIBUTING.md` and `SDLC.md`
- [ ] **CWPD-26** — Phase 2 Playwright tests (video tile grid, individual video pages, responsive breakpoints)
- [ ] **New initiative** — Release branch deployment strategy (`develop` → `main` with PO sign-off gate)

---

## Session 3 Plan

### Priority order

1. **Close all open Jira tickets** (session 1 + session 2 cleanup)
2. **Mark Jira version 1.0.0 as Released**
3. **CWPD-32** — Last TBD video (find URL, update file, commit)
4. **CWPD-25** — Definition of Done in CONTRIBUTING.md and SDLC.md
5. **CWPD-26** — Phase 2 Playwright tests
6. **CWPD-29** — Continue sourcing videos from the 20-video curriculum
7. **New initiative** — Release branch deployment strategy

---

## Current Ticket Status

| Ticket | Type | Status | Notes |
|--------|------|--------|-------|
| CWPD-1 | Initiative | Backlog | Close — PR #13 merged, v1.0.0 released |
| CWPD-2–4 | Epic | Backlog | Close — unblocked |
| CWPD-5 | Epic | Done | ✅ |
| CWPD-6 | Epic | Backlog | Close — unblocked |
| CWPD-7–17 | Story | Done | ✅ |
| CWPD-18–19 | Story | In Progress | Close — unblocked |
| CWPD-20–24 | Various | Backlog | CSS/SCSS migration — parked |
| CWPD-25 | Story | Backlog | Definition of Done — Session 3 |
| CWPD-26 | Story | Backlog | Phase 2 Playwright tests — Session 3 |
| CWPD-27 | Story | Backlog | Close — unblocked |
| CWPD-28 | Story | Done | ✅ Video library IDs — in production |
| CWPD-29 | Story | In Progress | 20-video curriculum — 10 done, ~10 remaining |
| CWPD-30 | Story | Done | ✅ YouTube rel=0 — in production |
| CWPD-31 | Story | Done | ✅ Video title font size — in production |
| CWPD-32 | Story | Backlog | Testing Best Practices video — TBD YouTube URL |
| CWPD-33 | Story | Done | ✅ Learn nav + page — in production |
| CWPD-34 | Story | Done | ✅ Learn page implementation — in production |
| CWPD-35 | Story | Done | ✅ CI audit trail — active |

---

## Technical Notes

- **Local dev:** `bundle exec jekyll serve --port 4001 --detach`
- **Kill Jekyll:** `pkill -f jekyll`
- **Run tests:** `npm test` (Jekyll must be running on port 4001)
- **Test count:** 14 tests across 3 spec files (navigation, promo-videos, services)
- **Test reports:** `tests/reports/html/` and `tests/reports/junit/results.xml` — gitignored locally, always uploaded in CI
- **Jira API:** Must use `Authorization: Basic <base64(email:token)>` header — curl `-u` flag unreliable
- **GitHub approver:** `simonhewinszodia` — second account for PR approvals
- **CI now triggers on:** every push to every branch (changed from PRs to main only)
- **Artifact naming:** `playwright-report-<commit-sha>` — permanently traceable
