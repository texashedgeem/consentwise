---
title: "Open Banking Sandbox Testing Isn't Enough: When You Need Real Bank Accounts"
description: "Why Open Banking sandboxes can't catch every integration bug, and how renting real, consenting UK bank accounts closes the gap before you go live or face FCA authorisation testing."
summary: "Why sandboxes miss the SCA quirks, consent-flow variations, and real account data that break integrations in production — and how to close the gap before FCA authorisation testing."
hero_image: annie-spratt-FSFfEQkd1sc-unsplash.jpg
date: 2026-07-28
---

Every Open Banking sandbox looks the same on paper: mocked accounts, canned balances, a consent screen that always says yes. That's fine for wiring up your first API call. It falls apart the moment you need to prove your integration survives contact with an actual bank.

## Where sandboxes stop being useful

Sandbox environments are built to be predictable, which is exactly their limitation. They rarely reproduce the things that break real integrations:

- **Strong Customer Authentication (SCA) quirks.** Every bank implements SCA slightly differently: different redirect timing, different session expiry windows, different failure messages when a user cancels partway through.
- **Consent journeys that vary bank to bank.** The screens, the wording, the number of steps between "connect my account" and a working access token are not standardised in practice, whatever the specification says.
- **Token and consent expiry behaviour.** Sandboxes tend to issue tokens that never expire, or expire on a schedule nothing like production. If your app doesn't handle re-consent gracefully, you won't find out until a real user hits it.
- **Genuinely variable account data.** Real accounts have real transaction histories, real edge cases in categorisation, real overdrafts and joint accounts. A mocked dataset can't surprise you the way a live one will.

None of this means sandboxes are pointless. They're the right place to build. They're the wrong place to convince yourself, or an FCA reviewer, that the integration actually works.

## What "renting" a real bank account solves

[ConsentWise's Consent for Rent service](/consent-for-rent/) gives developers access to real UK bank accounts, with the account holder's genuine consent, from £1 per bank per day with no contract. You run your actual AISP (account information) or PISP (payment initiation) flow end to end, against a real institution, with a real consent journey, and you can stop whenever the testing round is done.

The accounts themselves come from people who have opted in specifically to make their accounts available for this (ConsentWise's Agents programme). That matters for two reasons. First, it means the testing is genuinely consensual, not a workaround. Second, it means you're testing against ordinary consumer banking behaviour, not a curated demo account, which is closer to what your product will actually face in production.

## Who this is for

Three situations come up most often:

**Pre-authorisation testing.** If you're working toward FCA authorisation as an AISP or PISP, you need to show your integration handles real consent flows correctly, not just sandbox ones. Being able to point to genuine end-to-end test runs, on demand and without a long-term contract, is a cheaper and faster way to get there than negotiating test access with individual banks yourself.

**Pre-release regression testing.** Banks change their Open Banking implementations without much notice. A release that passed sandbox tests can still break against a specific bank's live SCA flow. Renting real accounts across a spread of banks before a release catches this before your users do.

**Bug hunting and edge cases.** ConsentWise also runs a Bug Hunt service and expert screensharing/troubleshooting support for teams that have found a live-only bug and need help reproducing or diagnosing it, not just more test accounts.

## How this fits with Payment Testing

Consent for Rent covers the AISP side: reading account data. [ConsentWise's Payment Testing service](/payment-testing/) covers the PISP side: initiating real payments from a real account, indicative pricing from £10 per transaction, again against genuine bank flows rather than a sandbox payment rail. The two are commonly used together for teams building products that both read and move money.

## Before you go live

Real bank testing tells you things a sandbox never will, but it isn't a substitute for your own security and compliance review. Treat it as the last integration check before authorisation or release, not the first thing you build against.

---

### FAQ

**Is this legal and compliant?**
The accounts used are provided by consenting account holders who have specifically opted in to make them available for testing (ConsentWise's Agents programme). You are testing against real consent, not bypassing it.

**Do I need a contract to start?**
No. Consent for Rent runs on a per-bank, per-day basis with no contract.

**How is this different from a sandbox?**
A sandbox uses mocked data and predictable behaviour. This uses real UK bank accounts with real SCA flows, real consent screens, and real transaction data, so it surfaces integration issues sandboxes are built to hide.

**What if I find a bug I can't reproduce reliably?**
ConsentWise's Bug Hunt and screensharing/troubleshooting services exist for exactly this: getting hands-on help with a live-only issue rather than just more test access.
