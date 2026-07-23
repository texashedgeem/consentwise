# ConsentWise — CLAUDE.md

## Current Focus

**Session 4: ticket closing sweep (CWPD-1,2,3,4,6,27,28,30,31,33,34,35,36,37), then CWPD-26 Phase 2 Playwright tests.**
Last session: Session 3, 13 Mar 2026. PR #18 merged. 0 In Progress, 39 Backlog.
> Update this section at the end of every session.

## Project Overview

- **Repo**: `texashedgeem/consentwise` (GitHub)
- **Live site**: https://consentwise.io
- **Local path**: `/Users/simonhewins/repo_git/consentwise`
- **Stack**: Jekyll → GitHub Pages. **Corrected 23 Jul 2026:** GitHub Pages actually
  deploys from `feature/CWPD-1-v1-release`, not `main` — `main` is stale and missing
  `/learn`, the video pages, and this file. Push to `main` does **not** auto-deploy.
  Confirm/resolve this before trusting the old assumption anywhere else.
- **Local dev**: `bundle exec jekyll serve --port 4001 --detach` (port 4000 often in use)

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
- **Playwright**: `npm test` — requires Jekyll on port 4001. 14 tests across 3 specs.
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
