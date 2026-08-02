# ConsentWise — CLAUDE.md

## Current Focus

**Snapshot reconciliation, 2 Aug 2026 — Current Focus had drifted since Session 3 (13 Mar 2026); this replaces it with where things actually stand today, not a full session-by-session history (45 commits happened in between — see `git log` or GrowthOS's `governance/decision-log.md` for that detail).**
- **Live site**: consentwise.io on GitHub Pages/Jekyll (unchanged), day-to-day managed by GrowthOS (`qeetoto_marketing_ceo` repo), which onboarded ConsentWise as a client 23 Jul 2026 (D-027).
- **`main` branch protection is PERMANENTLY relaxed** (required PR review = 0) — this is a standing decision (D-071, 1 Aug 2026), not "until further notice." Do not treat the restore command below as a pending action.
- **Analytics**: GA4 live since 23 Jul 2026, Consent Mode v2 (default-denied), confirmed reporting real visitor data as of 31 Jul 2026 (D-064).
- **SEO**: sitemap, robots.txt, meta descriptions, Organization+Service JSON-LD with pricing, live since 23 Jul 2026.
- **Content**: 9 guides published under `/guides` (new Jekyll collection + layout), governed by a standing "notify-after" publishing grant (PL-18) — GrowthOS can publish new guides in this lane without asking each time.
- **Internal-traffic exclusion**: a `?internal=1`/localStorage flag keeps GrowthOS's own testing out of GA4 (CWPD-78, merged 31 Jul 2026).
- **Jekyll-to-Vercel/Next.js migration**: evaluated and parked, no work scheduled.
- **Cookieless analytics baseline (Cloudflare Web Analytics)**: proposed and parked, not implemented.
- **Jira**: 0 In Progress, 57 Backlog, 26 Done (CWPD project, live count 2 Aug 2026).

For detail on any of the above, see `qeetoto_marketing_ceo/backlog.md`'s C-* rows and `governance/decision-log.md` — this repo's own `development_session_log/` hasn't been kept current since Session 3; that gap is real and not fixed by this snapshot alone.
> Update this section at the end of every session.

## Project Overview

- **Repo**: `texashedgeem/consentwise` (GitHub)
- **Live site**: https://consentwise.io
- **Local path**: `/Users/simonhewins/repo_git/consentwise`
- **Stack**: Jekyll → GitHub Pages (legacy build, source = `main` — confirmed via
  `gh api repos/texashedgeem/consentwise/pages` 23 Jul 2026). Push to `main`
  auto-deploys, as originally documented. `feature/CWPD-1-v1-release` is a long-lived
  dev branch — work lands there first and reaches production via PR into `main` (see
  PR #18, merged 13 Mar 2026, for the pattern). A same-day correction was briefly
  written here claiming Pages deployed from the feature branch — that was wrong
  (caused by checking a stale, unfetched local `main` ref) and has been reverted.
- **`main` branch protection — currently RELAXED (23 Jul 2026, standing, "until
  further notice"):** required PR reviews normally = 1 (approver: `simonhewinszodia`,
  Simon cannot self-approve) + passing Playwright status check + `enforce_admins:
  true`. The review requirement was dropped to 0 by owner instruction and, unlike an
  earlier same-day episode where it was restored right after a merge, this time it was
  **left off deliberately**. That means `main` can currently be merged into by anyone
  with push access with no review at all — treat this as a real, live gap, not a
  formality. Restore with: `gh api -X PATCH
  repos/texashedgeem/consentwise/branches/main/protection/required_pull_request_reviews
  -F dismiss_stale_reviews=true -F require_code_owner_reviews=false -F
  require_last_push_approval=false -F required_approving_review_count=1`. See
  `qeetoto_marketing_ceo/governance/decision-log.md` D-031/D-033 for the full history.
- **Local dev**: `bundle exec jekyll serve --port 42005 --detach` (project id 05, apisaurus PORT-REGISTRY.md, ADR 0002 — was 4001, which had collided with hedgeem-v7)

## Jira

- **Instance**: https://open-banking.atlassian.net
- **Project**: CWPD (ConsentWise Platform Development — Kanban, company-managed)
- **Auth**: simon.hewins@gmail.com + $JIRA_TOKEN (NOT $JIRA_ZODIA)
- **CRITICAL**: Use `Authorization: Basic <base64(email:token)>` — curl `-u` flag fails
- **CRITICAL**: Use POST `/rest/api/3/search/jql` (not GET)
- **Transition IDs**: Backlog=11, Selected=21, In Progress=31, Done=41
- **Hierarchy**: Initiative (10017) > Epic (10000) > Story (10016)
- **Priority model**: Initiatives=Medium, Epics and Stories=Low

## SDLC

- **Pre-commit hook**: `.githooks/commit-msg` — format: `TYPE[!](CWPD-NNN): description`
- **Activate hook on new clone**: `git config core.hooksPath .githooks`
- **Playwright**: `npm test` — requires Jekyll on port 42005. 14 tests across 3 specs.
- **CI**: `.github/workflows/ci.yml` — runs on every push
- **Release**: `feat!(CWPD-NNN):` → major, `feat(` → minor, all else → patch
- **Approver**: `simonhewinszodia` GitHub account (Simon cannot self-approve)

## Claude Behaviour Standards

- **Session start**: Read this "Current Focus" section and MEMORY.md. Announce next action. List In Progress CWPD tickets. Do this before anything else, without being asked.
- Show Jira preview before creating/updating tickets
- Add Jira comments at: start of work, description enhancement, Done transition, backlog decisions
- Never delete descriptions — only update or append
- Before closing any ticket: ask Simon if he wants to test first; capture response/evidence as a Jira comment before transitioning to Done
- $JIRA_TOKEN = open-banking.atlassian.net — do NOT use $JIRA_ZODIA here
- Always Edit files — never Write/overwrite
- Prompt before starting unticketted work
