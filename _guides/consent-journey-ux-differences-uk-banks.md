---
title: "Consent Journey UX Differences Across UK Banks: A Developer's Field Guide"
description: "Open Banking specifies what a consent journey must accomplish, not how it looks or how many steps it takes. Here's what actually varies bank to bank, and why it matters for your integration."
summary: "The specification says what a consent journey must accomplish, not how it looks or how many steps it takes. Here's what actually varies bank to bank."
icon: sliders
date: 2026-07-28
facts-verified: 2026-07-28
---

Open Banking standards define what a consent journey has to achieve: strong customer authentication, explicit consent, a way to revoke it later. They don't dictate the number of screens, the wording, or how long a session stays valid before it expires. Every bank fills in those details differently, and if you've only tested against one or two, the gap between what you expect and what a new bank actually does can be larger than it should be.

## Where the differences actually show up

**Number of steps.** Some banks complete SCA in two screens. Others split it across four or five, with intermediate confirmation steps a shorter flow skips entirely. If your UI assumes a fixed number of redirects, a bank with more steps will break that assumption.

**Redirect timing.** How quickly a bank redirects the user back to your app after consent varies, sometimes by several seconds. If your app has a tight timeout waiting for that redirect, a slower bank will trigger it unnecessarily.

**Session and token expiry windows.** Some banks issue short-lived tokens that expire quickly and expect frequent re-consent. Others last considerably longer. Code that assumes one behaviour will handle the other badly, either re-prompting a user who didn't need it or failing to re-prompt one who did.

**Cancellation and error messaging.** What a user sees, and what your app receives, when they cancel partway through differs meaningfully. Some banks send a clear cancellation signal your integration can act on immediately. Others are ambiguous, leaving your app to infer cancellation from a timeout or a generic error.

**Re-consent flows.** When consent expires and needs renewing, some banks make this nearly identical to first-time consent. Others streamline it noticeably for returning users, which changes what your app should expect and display.

## Why this matters more than it seems to at first

A consent journey that works cleanly against the bank you tested first often ships with quiet assumptions baked in: this many steps, this redirect speed, this error format. Those assumptions surface as real bugs the moment a customer connects a different bank, and because the underlying cause is a UX difference rather than a code defect in the traditional sense, it's often harder to diagnose from a stack trace alone.

## Building a genuine field guide for your own product

The only reliable way to learn these differences is to go through the consent journey yourself, deliberately, against a representative spread of UK banks, not just the one or two your team happens to bank with personally.

ConsentWise's [Consent for Rent](/consent-for-rent/) service makes this practical: real UK bank accounts, genuine consenting account holders through the Agents programme, from £1 per bank per day with no contract. Run the consent journey against several banks back to back and you'll build a real, specific picture of where your assumptions were wrong, rather than a generic list borrowed from documentation.

## What to actually record

For each bank you test, note the number of steps, the approximate redirect time, what a cancellation looks like from your app's side, and how re-consent behaves once the original consent expires. This is the closest thing to a real field guide for your specific integration, and it's usually more useful than any generic comparison, since it's built against exactly the flows your product actually triggers.

---

### FAQ

**Does the Open Banking specification allow this much variation?**
Yes. The specification defines outcomes (strong authentication, explicit consent, revocability) rather than a prescribed UI, so implementation details are left to each bank.

**How many banks should I test to get a representative picture?**
There's no fixed number, but testing against a single bank tells you almost nothing about how your integration handles the variation. Prioritise the banks your actual user base is most likely to use.

**Is this something the FCA or Open Banking body checks during authorisation?**
Not directly. This is a product-quality and reliability concern, not a formal regulatory requirement, but the underlying bugs it prevents are exactly the kind that show up as real customer-facing failures after launch.

**Should I test this myself or is it worth ConsentWise's expert troubleshooting service?**
Either can work. Testing it yourself with rented accounts builds direct product knowledge. If you're also debugging a specific issue you suspect is UX-related, [Screensharing](/expert-troubleshooting/) support can help isolate it faster.
