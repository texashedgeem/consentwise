---
date: 2026-03-09
time: 22:48
session_id: 5ec23c08-1eae-40c5-a14f-448dd76fd370
project: consentwise
type: release
---

# Release Notes — 2026-03-09

## Summary
Full migration of consentwise.io from a hosted WordPress/Cloudways instance to a zero-cost static site built with Jekyll and deployed via GitHub Pages, with Git-based content management replacing the CMS.

---

## What Was Delivered

### Site Migration
- Migrated all three public pages (Home, About Us, Services) with content and styles matching the original WordPress site verbatim
- Extracted and rewired the full WordPress theme CSS (372KB), replacing all Cloudways/WP asset paths with local `/assets/` references
- Migrated all static assets: logo SVG, hero video (16MB MP4), 15 images, and all third-party libraries (AOS, Lordicon, Owl Carousel, Slick, Google Fonts)

### Service Pages
- Created a `_services/` Jekyll collection with 8 individual Markdown files — one per service
- Each service is fully independently editable without touching any code
- Services: Consent for Rent, Payment Testing, Expert Troubleshooting, Bug Hunt, Consulting, Promo Videos, Bespoke Testing, Join Us
- Built `service.html` layout with hero image, body content, and related-services cross-linking
- Built `services/index.html` card grid dynamically driven by the collection

### Bug Fixes
- **Header transparency**: Fixed transparent header on non-home pages; now dark on all inner pages, transparent-on-load/dark-on-scroll on the home page only
- **About Us 404**: Added `permalink: /about-us/` front matter — Jekyll was building as `/about-us.html` not `/about-us/`
- **Service card image sizing**: Centre-cropped two mismatched images (portrait 1440×1800 and square 640×640) to consistent 3:2 ratio using Pillow
- **Mobile burger menu** (multi-stage fix):
  - Moved `<nav>` and overlay outside `<header>` to resolve CSS stacking context conflicts
  - Added `transform: none` CSS `!important` override to defeat theme's `translateX(100%)` off-screen hiding
  - Added `nav.classList.add('show')` to `openMenu()` so theme CSS transitions reveal li items correctly
  - Added `body.nav-open` CSS rules to drive overlay visibility and li item opacity

### Git & Deployment
- Repository created: `texashedgeem/consentwise` (public, GitHub)
- Custom domain `consentwise.io` configured via CNAME; DNS propagated at GoDaddy
- Rewrote full git history to attribute all commits to **Simon Hewins (texashedgeem)** with an "AI-Assisted" transparency trailer
- HTTPS via Let's Encrypt pending automatic provisioning by GitHub Pages (DNS is correctly configured; no action required)

### Testing
- Automated mobile testing via Playwright (iPhone 13 emulator) used throughout burger menu debugging to verify computed styles, z-indexes, element visibility, and screenshots without manual device testing

---

## Live URLs
- Site: http://consentwise.io (HTTPS activating automatically)
- Repo: https://github.com/texashedgeem/consentwise

---

## Known / Pending
- HTTPS enforcement not yet available in GitHub Pages settings — resolves automatically once Let's Encrypt cert is provisioned (typically within 24hrs of DNS being correct)
