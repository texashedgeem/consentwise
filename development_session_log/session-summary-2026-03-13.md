# ConsentWise Development Session Summary
**Date:** 13 March 2026
**Duration:** Full day session
**Repo:** texashedgeem/consentwise
**Session:** 3 of ongoing development

---

## Context

Session 3 picked up from the Session 2 plan. PR #17 was confirmed merged at session start. The session had two distinct themes: (1) SDLC hygiene — closing stale tickets, setting priorities, retroactively populating the GitHub Wiki, and fixing Jira ticket structure; (2) defining a formal "Claude-based SDLC" — creating a new initiative to document how Claude should behave in response to common commands, with stories that act as a living spec for AI-assisted development.

---

## What We Built Today

### Site UX — Hero Banners and Video Tiles

| # | Ticket | Change |
|---|--------|--------|
| 1 | CWPD-40/41/42 | Hero banner height reduced from ~500px to 300px on Services, About Us, and Learn pages — CSS: `.section-banner { height: 300px }` + `.section-banner .middle { padding-top: 75px }` for nav offset |
| 2 | CWPD-31 | Video tile h4 font size reduced 50% — `.video-tile-grid h4 { font-size: 1.5rem }` (was 3rem global) |
| 3 | — | Individual video page hero height fixed — `height: 200px; padding-top: 75px; box-sizing: border-box` + `h1 { font-size: 4rem }` |

### GitHub Actions Upgrades

| # | Change |
|---|--------|
| 1 | `actions/checkout` v4 → v6 (Node.js 24 compatible) |
| 2 | `actions/upload-artifact` v4 → v7 |
| 3 | `actions/setup-node` v4 → v6 |

### Release Notes Generator Improvements

| # | Feature |
|---|---------|
| 1 | Orphan ticket detection — Stories without Epic parent, Epics without Initiative parent |
| 2 | Open branches reporting — unmerged remote branches listed in release notes |
| 3 | v1.0.0 release notes regenerated with live Jira data (CWPD-1 now has fixVersion set) — GitHub Release body and audit JSON updated |

### GitHub Wiki

| # | What |
|---|------|
| 1 | Wiki enabled via GitHub API, initialised with git push |
| 2 | Release notes retroactively generated for all 17 versions (v0.1.0–v1.3.1) and pushed to wiki |
| 3 | `release.yml` updated — adds "Publish release notes to Wiki" step after every production deployment |
| 4 | Comprehensive `Home.md` written and published — 4 sections: SDLC Overview (8-step table with wiki links), Release History (last 10 releases), Compliance (ISO 27001 A.8.32/A.8.29/A.5.37, SOC 1 CC8.1/CC2.2/CC4.2, DORA Art.11/Art.25 — all with RAG status), Using Claude (placeholder) |

### Jira Structure

| # | What |
|---|------|
| 1 | All Epics linked to their Initiatives via "Relates" issue links (API parent not supported in company-managed Kanban without Jira Premium) |
| 2 | Platform Foundation Initiative (CWPD-53) created — CWPD-5 and CWPD-6 linked |
| 3 | All Stories and Epics set to Low priority — Initiatives set to Medium |
| 4 | CWPD-18 and CWPD-19 descriptions enhanced with full background, section breakdown, GitHub links, and ACs — both transitioned to Done |
| 5 | CWPD-25 updated with progress-to-date and conscious backlog decision note |
| 6 | CWPD-26 updated with Phase 1/Phase 2 breakdown, Playwright test references, screenshot attached |

### Define Claude SDLC Initiative (CWPD-47)

The most significant new addition this session — a formal initiative to document how Claude should behave in response to common SDLC commands. Stories act as a living spec.

| Ticket | Story |
|--------|-------|
| CWPD-49 | Define Claude's response to 'create a story' |
| CWPD-50 | Define Claude's response to 'enhance this description' |
| CWPD-52 | First steps — Getting started with Claude (CWPD-51 epic) |
| CWPD-54 | Train Claude to respond to 'regenerate release notes for release x' |
| CWPD-55 | Keep user focused on In Progress tickets |
| CWPD-56 | Add summary comments at key ticket lifecycle points |
| CWPD-57 | Define Claude's response to 'claude remind me' |

### New Behaviours Defined and Saved to Claude Memory

| Behaviour | Memory file |
|-----------|-------------|
| Always attach stories to an open Epic; create Epic/Initiative if none exists | `feedback_story_creation.md` |
| Proactively show In Progress tickets each session | `feedback_focus_inprogress.md` |
| Add Jira comments at key points (starting work, transitions, backlog decisions) | `feedback_ticket_comments.md` |
| 'claude remind me' — two-section memory + Jira status report | `feedback_claude_remind_me.md` |

### New Initiatives and Epics Created

| Ticket | Type | Summary |
|--------|------|---------|
| CWPD-43 | Initiative | Release notes and repository hygiene reporting |
| CWPD-44 | Initiative | Publish release notes to GitHub Wiki |
| CWPD-47 | Initiative | Define Claude based SDLC process and best practices |
| CWPD-53 | Initiative | Platform Foundation |
| CWPD-58 | Initiative | Release branch deployment strategy — develop to main with PO sign-off gate |
| CWPD-59 | Epic | Email release notes pipeline |
| CWPD-60–62 | Stories | Email release notes implementation stories |

### Stale Branch Cleanup

12 stale merged branches deleted from origin. Open branch tracking added to release notes generator so future unmerged branches are reported in every release.

---

## Things Simon Needs To Do

### Immediate

- [ ] **Ticket closing sweep** — CWPD-1, 2, 3, 4, 6, 27, 28, 30, 31, 33, 34, 35, 36, 37 are done work sitting in Backlog — transition to Done
- [ ] **CWPD-32** — Find YouTube URL for Open Banking Testing Best Practices (last TBD video)
- [ ] **CWPD-47 link in Jira UI** — Link CWPD-48 (Define Claude responses) and CWPD-51 (Getting started with Claude) Epics to CWPD-47 Initiative — API parent not supported, must be done manually

### Backlog

- [ ] **CWPD-26** — Phase 2 Playwright tests — transition to In Progress and start
- [ ] **CWPD-29** — Paste YouTube URLs to add remaining ~10 videos to curriculum
- [ ] **CWPD-52** — Populate video lists for steps 3 and 4 (Qasim list + curated list)

---

## Session 4 Plan

### Priority order

1. **Ticket closing sweep** — close all done-but-open tickets
2. **Transition CWPD-26 to In Progress** — Phase 2 Playwright tests is the primary development work
3. **CWPD-32** — source the last TBD video
4. **CWPD-29** — paste YouTube URLs to continue video curriculum
5. **CWPD-25** — Definition of Done (after CWPD-26 complete)

---

## Current Ticket Status

| Range | Status | Notes |
|-------|--------|-------|
| CWPD-1–6 | Backlog | Need closing — work complete |
| CWPD-7–19 | Done ✅ | |
| CWPD-20–24 | Backlog | CSS/SCSS migration — parked |
| CWPD-25 | Backlog | DoD — consciously parked pending CWPD-26 |
| CWPD-26 | Backlog | Phase 2 Playwright tests — next active dev ticket |
| CWPD-27–35 | Backlog/Done | Need closing sweep for open ones |
| CWPD-36–38 | Backlog | May be done — need review |
| CWPD-39–62 | Backlog | New initiatives, epics, stories created this session |

---

## Technical Notes

- **Session log folder:** `development_session_log/` (already existed from Session 2)
- **Wiki:** https://github.com/texashedgeem/consentwise/wiki — live with all 17 release notes + Home.md
- **Jira priority model:** Initiatives = Medium, everything else = Low
- **Claude memory files:** `/Users/simonhewins/.claude/projects/-Users-simonhewins-repo-git-consentwise/memory/`
- **Claude alias:** "claude remind me" — two-section report (memory analysis + live Jira status)
- **Release notes:** `scripts/generate_release_notes.py` — run with `JIRA_TOKEN=$JIRA_TOKEN python3 ...`
- **Jira Epic→Initiative parent:** Cannot set via API in company-managed Kanban — use "Relates" issue link instead, set parent manually in UI
