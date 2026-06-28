# Challenge: The honest split

## Scenario

Here is the moment that makes Cloud Capital different, and it is the hardest screen in
the product. The savings the commitment generates are split three ways: the customer's
**guaranteed share**, the **risk reserve**, and our **profit.** Our competitors hide
this; their edge depends on the customer never seeing it. Ours depends on the
opposite — we show it. But showing a vendor's margin to the customer paying it is a
knife's edge: done badly it reads as "look how much they're taking," and done well it
reads as "now I understand the deal, and it's fair." Your job is the second one.

## The task

Build the surface that presents the split honestly — what the customer keeps, what we
hold back as reserve, what we keep as profit — and makes the customer come away
**trusting** it. Not by hiding the numbers, but by making the *reasoning* legible: why
a reserve exists at all, what risk we're carrying on their behalf, why the split is
calibrated where it is, and how their guaranteed rate compares to the baseline they'd
reasonably expect.

## What makes it non-trivial

- **This is a product-communication problem first.** The numbers are given (the
  service's `/economics` hands you `customer_savings`, `reserve`, `profit`, and the
  `cost_of_risk_points` behind the reserve). The whole challenge is the framing: the
  same three numbers can build trust or destroy it depending on how you stage what the
  customer understands, and in what order.
- **The risk we bear is the part that justifies the split, and it's invisible by
  default.** We guarantee a rate and eat the downside when usage comes in low. A
  customer who doesn't grasp that sees only "they kept money." Making the risk *felt* —
  without overclaiming, and without a forecast (you don't have one) — is the design
  problem.
- **Honesty under exploration.** A customer who drills in from challenge 2 will land
  here. The split has to stay coherent and honest at every level of breakdown, not just
  in the summary.

## Deliverables

1. **The split surface** — customer share, reserve, and profit, presented so a
   non-technical user finishes informed and reassured rather than alarmed.
2. **The reasoning made legible** — why the reserve exists and what risk it covers,
   pitched at a layperson.
3. **A short note** on the framing decisions you made and what you deliberately chose
   *not* to do (the dark patterns available here, and why you declined them).

## What we're looking for

Taste and integrity in presenting data that cuts against your own side of the table.
This is where we learn whether you can make an honest interface that a customer trusts
*because* it's honest — the thing the whole company is betting on.

---

**References:** [scenario](../scenario.md) · [data contract](../data_contract.md). **With your submission:** an [understanding ledger](../understanding_ledger.md). See the [challenge overview](./README.md).
