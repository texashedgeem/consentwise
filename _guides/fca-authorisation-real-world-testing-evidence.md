---
title: "FCA Authorisation as an AISP or PISP: What 'Real World Testing' Evidence Actually Means"
description: "The FCA doesn't hand you a testing checklist for AISP or PISP authorisation, but your systems and controls review lives or dies on whether your integration actually works. Here's what real testing evidence looks like."
summary: "The FCA won't give you a testing checklist, but your authorisation review depends on proving your integration actually works. What real evidence looks like, and how to get it."
hero_image: annie-spratt-FSFfEQkd1sc-unsplash.jpg
date: 2026-07-28
facts-verified: 2026-07-28
---

Ask ten fintechs what "testing evidence" means for FCA authorisation and you'll get ten different answers. That's because the FCA doesn't publish a testing checklist for AISP or PISP applicants. What it does require is that you demonstrate adequate systems and controls: a working operational risk framework, appropriate governance, and the ability to safely handle customer data or funds from day one. Testing is how you prove that, not a separate box to tick.

## What the FCA actually asks for

Account Information Service Provider (AISP) registration is lighter than full authorisation. There's no initial capital requirement and no ongoing own-funds test, and the process typically runs four to six months. Payment Initiation Service Provider (PISP) permission is a different tier entirely: you need authorisation as a full Payment Institution, PSD2 service 7, and initial capital of €50,000.

Both routes share the same underlying question from the reviewer: can this firm's systems actually do what the application says they do? A Regulatory Business Plan full of architecture diagrams doesn't answer that. A working consent flow, run end to end against a real UK bank, does.

Worth knowing if you're mid-application: the FCA's new CASS 15 safeguarding regime comes into force on 7 May 2026 for UK API firms handling funds (AIS-only and PIS-only providers are exempt). If your firm falls under it, daily segregation monitoring and reconciliation become part of what you need to show works, not just describe.

## Why sandbox screenshots don't satisfy a reviewer

A sandbox demo proves your code compiles and your happy path renders. It doesn't prove your consent handling survives a bank's actual SCA implementation, a re-authentication after token expiry, or a user who cancels halfway through and comes back an hour later. Those are exactly the scenarios a reviewer, or worse, a real customer, will hit first.

Evidence that holds up under scrutiny tends to share three qualities:

- It's against a real, consenting UK bank account, not a mocked one.
- It covers more than one bank, since implementations genuinely differ.
- It's repeatable on demand, so you can show the same flow working again if asked.

## Getting there without a long-term test rig

Building your own ongoing access to real UK bank accounts for testing means negotiating with banks directly, something most applicants aren't positioned to do before they're even authorised. ConsentWise's [Consent for Rent](/consent-for-rent/) service exists for exactly this gap: real UK bank accounts, genuine account holder consent through the Agents programme, from £1 per bank per day, no contract. Run your AISP flow end to end, across several banks, and keep the record.

If your application also covers payment initiation, [Payment Testing](/payment-testing/) covers the PISP side the same way, with indicative pricing from £10 per transaction.

## Before you submit

Testing evidence isn't the whole application, and it won't substitute for a properly built Regulatory Business Plan or adequate governance structure. Treat it as the part of the application you can make undeniable: proof, not just a description, that the integration works against reality.

---

### FAQ

**Does the FCA require a specific testing document format?**
No. There's no published testing checklist. What matters is that your systems and controls review holds up, and real end-to-end evidence is the most direct way to support that.

**Is AISP registration the same process as PISP authorisation?**
No. AISP (or RAISP) registration is lighter, with no initial capital requirement and a faster typical timeline. PISP requires full Payment Institution authorisation under PSD2 service 7, including €50,000 initial capital.

**Do I still need eIDAS certificates as a UK TPP?**
Not in the same way as before Brexit. The FCA introduced an alternative identification approach for UK-based TPPs after eIDAS certificates issued under the EU regime stopped being valid for UK firms at the end of the transition period.

**What if my firm falls under the new CASS 15 safeguarding regime?**
CASS 15 comes into force 7 May 2026 for UK API firms that hold funds (AIS-only and PIS-only providers are excluded). It requires daily segregation monitoring and regular reconciliation, on top of the usual safeguarding duties.
