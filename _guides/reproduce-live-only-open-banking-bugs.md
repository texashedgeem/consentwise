---
title: "How to Reproduce a Live-Only Open Banking Bug (Without Guessing)"
description: "Some Open Banking bugs only show up against real bank accounts and never reproduce in a sandbox. Guessing at the cause wastes time. Here's a more reliable way to isolate and confirm the fix."
summary: "Some bugs only show up against real bank accounts and never reproduce in a sandbox. Guessing at the cause wastes time. A more reliable way to isolate and confirm the fix."
icon: bug
date: 2026-07-28
facts-verified: 2026-07-28
---

Every Open Banking team eventually hits the same frustrating pattern: a bug report from production that won't reproduce in the sandbox, no matter how carefully you retrace the reported steps. The sandbox account behaves fine. The code review turns up nothing obvious. The bug is real, a customer genuinely hit it, but it's invisible in every environment you actually control.

This happens because sandboxes are built to be predictable, and the bugs that only appear live are, almost by definition, the ones caused by something unpredictable: a specific bank's SCA timing, a consent token that expired at an unusual moment, an account state the sandbox never models.

## Why guessing at the cause wastes more time than it saves

The instinct is to read the error log, form a theory, patch the most likely cause, and ship the fix. Without being able to reproduce the bug, that patch is unverified. If the bug doesn't recur, you don't know whether you fixed it or whether it was simply rare enough not to hit again yet. If it does recur, you've spent a release cycle on a guess.

The more reliable path is narrower and less satisfying in the short term: reproduce the bug first, confirm the fix against the same conditions, then ship.

## Getting from "unreproducible" to "reproduced"

Start by narrowing what's actually specific to the failure. Was it one particular bank, or several? A specific account type, business versus personal? A particular point in the consent lifecycle, close to token expiry, immediately after re-authentication, or during a re-consent flow? The more precisely you can characterise the conditions, the smaller the gap you need to close between "sandbox" and "reality."

From there, reproducing it requires running your actual integration against a real account matching those conditions, not a mock of them. If the bug is bank-specific, that means testing against that specific bank, not a generic one. If it's tied to token expiry timing, that means letting a real token actually expire under real conditions rather than simulating expiry in code.

## Where ConsentWise fits

Getting access to the specific real-world conditions a bug needs, a particular bank, a particular account state, on demand, is exactly what ConsentWise's [Bug Hunt](/bug-hunt/) and [Screensharing](/expert-troubleshooting/) services are built for. Rather than guessing which bank or account condition triggered the issue, you get hands-on help isolating and reproducing it against real infrastructure, with someone who has seen a wide range of these live-only failure modes before.

If the bug turns out to need broader testing once it's understood, for instance confirming the fix holds across several banks, not just the one where it first appeared, [Consent for Rent](/consent-for-rent/) and [Payment Testing](/payment-testing/) extend that into a proper regression pass across real accounts.

## After you've reproduced it

Confirming the fix matters as much as finding the bug. Once you can reliably reproduce the failure, verify your patch actually stops it under the same real conditions, not just in the sandbox where the original bug never showed up in the first place. A fix you've only tried in that sandbox is still a guess, however confident it feels.

---

### FAQ

**What kinds of bugs are most likely to be live-only?**
Anything tied to SCA timing, token or consent expiry, re-authentication flows, or account states a sandbox doesn't model (overdrafts, joint accounts, unusual transaction histories) is a strong candidate for a bug that won't reproduce outside real conditions.

**Do I need to already know which bank caused the issue before asking for help?**
No. Part of the value of expert troubleshooting is narrowing that down when you don't yet know, rather than needing the diagnosis done before you ask.

**Is Bug Hunt different from ongoing testing services like Consent for Rent?**
Yes. Bug Hunt and expert troubleshooting are focused on isolating and reproducing a specific known issue. Consent for Rent and Payment Testing are broader, ongoing access to real accounts for ordinary testing and regression work.

**How do I confirm a fix actually worked, not just that the bug didn't recur immediately?**
Reproduce the original failure conditions again, deliberately, after deploying the fix, rather than waiting to see if it happens again in production. That's the only way to know the fix addressed the actual cause.
