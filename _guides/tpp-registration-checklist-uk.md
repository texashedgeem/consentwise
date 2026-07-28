---
title: "TPP Registration Checklist: What UK Regulators Actually Check Before You Go Live"
description: "A practical walkthrough of what UK Third Party Provider registration actually involves, from FCA authorisation type to Open Banking Directory onboarding, and where real testing fits in."
summary: "What UK Third Party Provider registration actually involves, from choosing the right FCA authorisation type to Open Banking Directory onboarding, and where real testing fits."
hero_image: annie-spratt-FSFfEQkd1sc-unsplash.jpg
date: 2026-07-28
facts-verified: 2026-07-28
---

Becoming a registered Third Party Provider (TPP) in the UK isn't one step, it's a sequence of separate registrations that each unlock the next. Teams new to Open Banking often assume FCA authorisation alone is enough. It isn't. Here's the actual order of operations.

## 1. Choose the right FCA permission

This is the first fork in the road, and it determines almost everything downstream.

**Account Information Service Provider (AISP)**, sometimes registered as a Registered Account Information Service Provider (RAISP), is the lighter route: no initial capital requirement, no ongoing own-funds test, and a typical registration timeline of four to six months.

**Payment Initiation Service Provider (PISP)** is a heavier tier. It requires full authorisation as a Payment Institution under PSD2 service 7, with initial capital of €50,000, alongside a larger and more detailed application file.

Get this choice wrong and you'll either apply for more regulatory burden than you need, or find out mid-application that your product actually requires the heavier route.

## 2. Build the systems and controls your application will be judged on

The FCA doesn't sign off on architecture diagrams. It wants evidence of adequate financial resources, suitable risk management, appropriately competent people, and proper governance structures around the service you're actually planning to run. Firms handling funds should also be aware of the new CASS 15 safeguarding regime coming into force on 7 May 2026, which requires daily segregation monitoring and reconciliation (AIS-only and PIS-only providers are excluded).

## 3. Identify yourself to banks correctly

Once authorised or registered, you still need a way to prove your identity to every bank you connect to. Before Brexit, this ran through eIDAS certificates issued under the EU regime. Those certificates stopped being valid for UK-only TPPs once the transition period ended, and the FCA introduced an alternative identification approach for UK firms instead. If any part of your business also operates across the EU, check which identification route applies where, since the UK and EU paths have diverged.

## 4. Onboard to the Open Banking Directory

UK banks won't grant API access to a TPP they can't verify. The Open Banking Directory is where that verification happens: a valid identification credential gets uploaded, a Software Statement Assertion is generated, and that's what actually lets you register and connect with individual banks' APIs in production. Skipping or rushing this step is a common reason integrations that work in a sandbox don't work against real bank endpoints.

## 5. Prove the integration actually works

This is the step regulators, and your own product roadmap, care about most, and it's the one a checklist alone can't satisfy. A consent flow that works against a mocked sandbox account tells you almost nothing about how it behaves against a real bank's SCA implementation, real token expiry, or a real user cancelling partway through.

ConsentWise's [Consent for Rent](/consent-for-rent/) service exists for this exact gap: real UK bank accounts, genuine consenting account holders through the Agents programme, from £1 per bank per day with no contract. If your registration also covers payment initiation, [Payment Testing](/payment-testing/) covers that side the same way.

## Putting it together

The order matters. Choosing the wrong FCA permission wastes months. Skipping proper systems and controls work invites a rejected application. Getting Directory onboarding wrong means your API calls fail for reasons that have nothing to do with your code. And treating real-bank testing as optional, rather than as the thing that proves everything above actually works, is the most common way teams find out about a problem after they've gone live instead of before.

---

### FAQ

**Do I need to register as both an AISP and a PISP?**
Only if your product genuinely does both: reads account information and initiates payments. Many products only need one, and applying for permissions you don't need adds unnecessary regulatory burden.

**Is Open Banking Directory registration part of FCA authorisation, or separate?**
Separate. FCA authorisation or registration is a regulatory step. Directory onboarding is a technical one that happens afterwards, using the credentials your FCA status makes you eligible for.

**Do UK TPPs still need eIDAS certificates?**
Not in the original form. UK-only TPPs use an FCA-introduced alternative identification approach post-Brexit. Firms with EU operations should check both regimes separately, since they've diverged.

**What's the most common reason a working sandbox integration fails against real banks?**
Directory onboarding issues and untested edge cases in SCA and consent flows are the two most common causes. Both are things real-bank testing catches before a rejected application or a broken production launch does.
