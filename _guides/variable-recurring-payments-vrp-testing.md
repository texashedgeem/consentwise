---
title: "Variable Recurring Payments (VRP) Testing: What Sandboxes Get Wrong"
description: "VRP consent setup and individual payment execution are two separate flows with different failure modes. Sandboxes tend to simplify both. Here's what to actually test."
summary: "VRP consent setup and each individual payment are separate flows with different failure modes, and sandboxes tend to flatten both into one simplified path."
icon: repeat
date: 2026-07-28
facts-verified: 2026-07-28
---

Variable Recurring Payments let a customer authorise your product to make a series of payments within agreed limits, without re-approving every single one. It's a genuinely useful capability for anything from bill splitting to automated savings, and it's also more complex to test properly than a one-off payment, because there are two separate flows involved and sandboxes tend to blur the line between them.

If you want the broader context on VRP as a concept, ConsentWise's [Open Banking video library](/learn/) covers the fundamentals. This guide focuses specifically on what to test once you're building against it.

## Two flows, two sets of failure modes

**The consent setup flow** is where the customer authorises the ongoing arrangement: the payment limits, the frequency, and the duration. This happens once, or infrequently, and it's the flow most sandboxes simulate reasonably well because it resembles a standard consent journey.

**Individual payment execution** happens repeatedly, potentially many times, against that standing consent. This is where real testing diverges sharply from sandbox behaviour, because each execution needs to correctly check against the agreed limits without asking the customer to re-authenticate.

Testing only the first flow and assuming the second works the same way is the most common mistake teams make with VRP.

## What breaks in practice

- **Limit enforcement drift.** A payment that should be rejected for exceeding the agreed limit sometimes isn't, especially at the exact boundary value. Sandboxes rarely simulate boundary conditions accurately.
- **Consent expiry mid-arrangement.** If the standing consent expires or the customer revokes it between payments, your product needs to detect that gracefully rather than silently failing or retrying indefinitely.
- **Frequency validation.** Banks enforce the agreed frequency differently. A payment attempted slightly outside the agreed window can be accepted by one bank's implementation and rejected by another's.
- **Bank-specific VRP maturity.** Not every bank's VRP implementation behaves identically, since this is a newer capability than basic single payments. Some edge cases only appear against specific banks.

## Testing this properly

Real VRP testing means setting up a genuine standing consent against a real UK bank account, then executing multiple payments over time against it, deliberately including at least one that should be rejected (over the limit, outside the frequency window, or after consent expiry) to confirm your product handles rejection correctly rather than just testing the happy path repeatedly.

ConsentWise's [Consent for Rent](/consent-for-rent/) service supports this: real, consenting UK bank accounts from £1 per bank per day, no contract, so you can run a full VRP consent-and-execution cycle rather than a single simulated payment. Testing across more than one bank matters more here than for single payments, given how much VRP implementation maturity still varies.

## A practical testing sequence

Start by confirming the consent setup flow completes correctly and the agreed limits are recorded as expected. Then execute a payment comfortably within those limits and confirm it succeeds. Follow with a payment intentionally over the limit and confirm your product surfaces the rejection correctly rather than treating it as a generic error. Finally, if your timeline allows, test what happens when the standing consent is revoked mid-arrangement, since this is the scenario most products handle worst in production.

---

### FAQ

**Is VRP the same as a standing order or Direct Debit?**
No. VRP happens through Open Banking's API rather than the bank's own recurring payment rails, and it gives your product more direct control over individual payment execution within the agreed limits.

**Do I need a separate FCA permission for VRP specifically?**
VRP falls under the same PISP permission that covers payment initiation generally. There isn't a distinct VRP-specific authorisation category.

**How many payments should I test before I'm confident the arrangement works?**
Enough to cover at least one within-limit success, one over-limit rejection, and ideally one execution after a meaningful time gap, to confirm the standing consent behaves correctly over time rather than just immediately after setup.

**Can I test VRP and single payments with the same rented account?**
Yes. Consent for Rent doesn't restrict what payment flows you test against the account, so a single testing round can cover both if needed.
