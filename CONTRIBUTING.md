# Contributing to ConsentWise

This document covers everything needed to contribute to the ConsentWise Jekyll site — local setup, branching, commit conventions, testing, and the PR process.

---

## Table of Contents

1. [Local setup](#local-setup)
2. [Branching strategy](#branching-strategy)
3. [Commit message format](#commit-message-format)
4. [Running tests locally](#running-tests-locally)
5. [Pull request process](#pull-request-process)
6. [CI pipeline](#ci-pipeline)

---

## Local setup

### Prerequisites

| Tool | Version | Notes |
|------|---------|-------|
| Ruby | 3.x | Install via Homebrew: `brew install ruby` |
| Bundler | latest | `gem install bundler` |
| Node.js | 18+ | Install via [nodejs.org](https://nodejs.org) or `brew install node` |
| npm | bundled with Node | — |

### First-time setup

```bash
# 1. Clone the repo
git clone https://github.com/texashedgeem/consentwise.git
cd consentwise

# 2. Activate the pre-commit hook
git config core.hooksPath .githooks

# 3. Install Ruby dependencies
bundle install

# 4. Install Node dependencies and Playwright browsers
npm install
npx playwright install chromium
```

> **Note:** `node_modules/` is gitignored. Run `npm install` after every fresh clone.

### Running the site locally

```bash
bundle exec jekyll serve --port 4001
```

The site is available at [http://localhost:4001](http://localhost:4001). Port 4001 is used intentionally — port 4000 is often occupied by other tools.

---

## Branching strategy

All work branches off `main`. Branch names follow this pattern:

```
feature/CWPD-NNN-short-description
```

Examples:
```
feature/CWPD-7-videos-collection
feature/CWPD-12-youtube-embed
```

- One branch per Jira story
- Never commit directly to `main` — it is protected and requires an approved PR
- Keep branches short-lived; merge as soon as the story is complete

---

## Commit message format

All commits must follow the **Conventional Commits** format referencing the Jira ticket. This is enforced by a pre-commit hook (`.githooks/commit-msg`).

```
TYPE(CWPD-NNN): short description
```

### Valid types

| Type | Use for |
|------|---------|
| `feat` | New feature or user-visible change |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `test` | Adding or updating tests |
| `ci` | CI/CD pipeline changes |
| `chore` | Build, config, or dependency changes |
| `style` | CSS or formatting changes with no logic change |
| `refactor` | Code restructuring with no behaviour change |

### Examples

```
feat(CWPD-10): add video tile grid to /promo-videos/ page
fix(CWPD-11): correct tile hover colour on mobile
docs(CWPD-18): add branching strategy to CONTRIBUTING.md
test(CWPD-14): add Playwright tests for services page
ci(CWPD-16): add GitHub Actions CI pipeline
```

### Hook behaviour

- Merge commits and fixup/squash commits are automatically allowed
- Any other commit that does not match the pattern is **rejected at commit time**
- The hook must be activated once per clone: `git config core.hooksPath .githooks`

---

## Running tests locally

Tests use [Playwright](https://playwright.dev) and run against the local Jekyll server.

### Before running tests

The Jekyll server must be running on port 4001:

```bash
bundle exec jekyll serve --port 4001
```

### Run all tests

```bash
npm test
```

### View the HTML report after a run

```bash
npm run test:report
```

### Test structure

```
tests/
  e2e/
    pages/
      services.spec.js       # Services page functional tests
      promo-videos.spec.js   # Promo Videos page functional tests
  helpers/
    navigation.js            # Shared helpers (waitForPageLoad, getTiles)
  reports/                   # Generated HTML report (gitignored)
```

Tests run in headless Chromium only. Screenshots are captured automatically on failure.

---

## Pull request process

1. **Create a branch** off `main` using the naming convention above
2. **Make your changes** — all commits must pass the pre-commit hook
3. **Run tests locally** and confirm they pass before pushing
4. **Push and open a PR** targeting `main`
5. **Request a review** — PRs require 1 approving review before merge
6. **PR authors cannot approve their own PRs** — a second reviewer must approve
7. **Merge** once approved and all CI checks pass

### PR title format

Match the commit format:

```
feat(CWPD-10): add video tile grid to /promo-videos/ page
```

---

## CI pipeline

Every PR to `main` triggers the GitHub Actions CI workflow (`.github/workflows/ci.yml`):

1. Checks out the code
2. Installs Ruby dependencies and builds Jekyll
3. Installs Node dependencies and Playwright browsers
4. Starts the Jekyll server on port 4001
5. Runs the full Playwright test suite
6. On failure: uploads the HTML test report as a downloadable artifact (7 day retention)

PRs cannot be merged if CI is failing.

On merge to `main`, a second workflow (`.github/workflows/release.yml`) automatically:
- Increments the semver version (`feat` → minor bump, all others → patch bump)
- Generates categorised release notes with Jira ticket hyperlinks
- Creates a GitHub Release and tag
