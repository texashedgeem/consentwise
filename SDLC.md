# Software Development Lifecycle (SDLC) — ConsentWise

**Document owner:** Qeetoto Limited
**Last reviewed:** March 2026
**Version:** 1.0
**Classification:** Internal

---

## 1. Purpose and Scope

This document describes the Software Development Lifecycle (SDLC) controls in place for the ConsentWise platform (`consentwise.io`). It is intended to provide evidence of a controlled, auditable development process aligned with the requirements of:

- **ISO/IEC 27001:2022** — particularly Annex A controls covering secure development and change management
- **SOC 1 Type II** — Change Management criteria (CC8.1)
- **DORA** (Digital Operational Resilience Act) — ICT change management and testing obligations

The scope covers all changes to the ConsentWise Jekyll website hosted on GitHub Pages, managed within the GitHub repository `texashedgeem/consentwise`.

---

## 2. SDLC Overview

All changes follow a linear, gated lifecycle:

```
Backlog (Jira)
    ↓
Feature branch created
    ↓
Development with commit traceability
    ↓
Pre-commit hook validation
    ↓
Pull request opened
    ↓
Automated CI tests (Playwright)
    ↓
Peer review and approval
    ↓
Merge to main
    ↓
Automated release and deployment (GitHub Pages)
    ↓
Release notes generated
```

No change reaches production without passing every gate.

---

## 3. Work Item Tracking and Traceability

All development work is tracked in **Jira** (project: `CWPD`, instance: `open-banking.atlassian.net`).

### Ticket Hierarchy

| Level | Type | Purpose |
|-------|------|---------|
| 1 | Initiative | Business objective grouping multiple epics |
| 2 | Epic | A cohesive deliverable within an initiative |
| 3 | Story | A single unit of work, completable in one branch/PR |

### Traceability

Every commit references its Jira story ticket using the enforced commit format (see Section 5). This creates a bidirectional audit trail:

- From **Jira story → Git commit(s) → PR → GitHub Release**
- From **GitHub Release → commit list → Jira story** (via hyperlinks in release notes)

---

## 4. Branching Strategy

| Branch | Purpose | Direct commits allowed? |
|--------|---------|------------------------|
| `main` | Production-ready code, auto-deployed to GitHub Pages | No — protected |
| `feature/CWPD-NNN-*` | One branch per Jira story | Yes |

**Branch protection rules on `main`:**
- Minimum 1 approving review required before merge
- Stale reviews dismissed when new commits are pushed
- Force push and branch deletion blocked

---

## 5. Commit Standards

All commits must follow the **Conventional Commits** specification with mandatory Jira ticket reference:

```
TYPE(CWPD-NNN): short description
```

Valid types: `feat` | `fix` | `docs` | `test` | `ci` | `chore` | `style` | `refactor`

This format is **automatically enforced** by the pre-commit hook at `.githooks/commit-msg`. Non-compliant commits are rejected at the point of commit, before code can reach the remote repository.

The hook must be activated on each clone: `git config core.hooksPath .githooks` (documented in `CONTRIBUTING.md`).

---

## 6. Testing

### Automated Functional Tests

Functional tests are written using [Playwright](https://playwright.dev) and reside in `tests/e2e/`. Tests run in headless Chromium against the Jekyll development server.

| Command | Purpose |
|---------|---------|
| `npm test` | Run full test suite |
| `npm run test:report` | Open HTML test report |

### CI Execution

Tests run automatically on every pull request via GitHub Actions (`.github/workflows/ci.yml`). The pipeline:

1. Installs Ruby dependencies and builds Jekyll
2. Installs Node dependencies and Playwright browsers
3. Starts Jekyll on port 4001 and waits for readiness
4. Executes the full Playwright test suite
5. On failure: uploads the HTML report as a downloadable artifact (7 day retention)

**A PR cannot be merged if CI is failing.**

### Test Coverage

Tests validate functional behaviour of key user-facing pages. New pages and features require accompanying tests before a story can be considered complete.

---

## 7. Code Review and Approval

All changes require a **peer review** via GitHub pull request before merging to `main`.

| Control | Implementation |
|---------|---------------|
| Minimum reviewers | 1 approving review required |
| Self-approval | Not permitted — PR authors cannot approve their own PRs (GitHub platform control) |
| Stale review dismissal | Approvals are dismissed if new commits are pushed after approval |
| Review scope | Reviewer is responsible for verifying code correctness, security, and adherence to standards |

---

## 8. Deployment

Deployment is continuous and automatic:

- Every merge to `main` triggers a **GitHub Pages** deployment
- No manual deployment steps exist — this eliminates human error in the release process
- Deployments are visible in the GitHub repository's **Deployments** tab, providing an audit log of every production change

---

## 9. Release Management

Every merge to `main` triggers the release workflow (`.github/workflows/release.yml`), which automatically:

1. Computes the next **semantic version** based on commit types:
   - `feat` commits → minor version bump (e.g. v1.1.0 → v1.2.0)
   - All other types → patch version bump (e.g. v1.1.0 → v1.1.1)
2. Generates **categorised release notes** from the commit log
3. Hyperlinks every `CWPD-NNN` reference to the corresponding Jira story
4. Creates a **GitHub Release** and version tag

This provides a complete, immutable record of every production release, linking business requirements (Jira) to the technical changes delivered.

---

## 10. Control Summary

The table below maps implemented controls to relevant framework requirements.

| Control | Implementation | ISO 27001:2022 | SOC 1 | DORA |
|---------|---------------|----------------|-------|------|
| Work item tracking | Jira CWPD project | A.8.32 | CC8.1 | Art. 11 |
| Commit traceability | Conventional commits + pre-commit hook | A.8.32 | CC8.1 | Art. 11 |
| Branch protection | GitHub branch protection on `main` | A.8.32 | CC8.1 | Art. 11 |
| Automated testing | Playwright via GitHub Actions CI | A.8.29 | CC8.1 | Art. 25 |
| Peer review | PR approval required, no self-approval | A.8.32 | CC8.1 | Art. 11 |
| Automated deployment | GitHub Pages on merge to main | A.8.32 | CC4.2 | Art. 11 |
| Release audit trail | GitHub Releases with Jira links | A.8.32 | CC8.1 | Art. 11 |
| Documented procedures | CONTRIBUTING.md, SDLC.md | A.5.37 | CC2.2 | Art. 11 |

### ISO 27001:2022 References
- **A.5.37** — Documented operating procedures
- **A.8.29** — Security testing in development and acceptance
- **A.8.32** — Change management

### SOC 1 References
- **CC2.2** — Information and communication (documented policies)
- **CC4.2** — Monitoring controls
- **CC8.1** — Change management — authorisation, testing, approval, and implementation

### DORA References
- **Article 11** — ICT change management policy
- **Article 25** — Testing of ICT tools, systems, and processes

---

## 11. Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | March 2026 | Qeetoto Limited | Initial release |
