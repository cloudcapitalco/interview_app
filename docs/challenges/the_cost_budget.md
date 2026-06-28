# Challenge: The cost budget

> Hard. Takes the centerpiece decision and makes it quantitative, under pressure.

## Scenario

What you built in [Ask and explain](./ask_and_explain.md) works on one customer's
data with you watching. Production is every customer, all day, at a scale where every
fraction of a cent and every hundred milliseconds is multiplied by a number that would
make your eyes water. A decision that felt reasonable in a demo can be indefensible at
scale — and "it works" is not the same claim as "it works inside a budget."

## The task

Put a number on it. Given an explicit budget — say, a target like **a p95 answer
under two seconds and under a cent per question, holding at a customer one to two
orders of magnitude larger than the one you were given** — show how your design holds,
where it breaks, and what you change to keep it inside the line. Pick concrete targets
if these aren't the right ones; the point is to commit to numbers and reason against
them, not to hit a specific figure.

## What makes it non-trivial

- **You have to measure, not assert.** What does a question actually cost you today —
  in tokens, in latency, in dollars — and where does that go as volume and customer
  count climb? Measure the whole path, including what you pay to get the economics in
  the first place (the [service](../../service/README.md) is part of your latency and
  cost budget, not free). An answer without numbers is the failure mode this challenge
  exists to catch.
- **The levers trade against each other.** More caching and templating buys cost and
  latency and spends flexibility; more model spends flexibility and costs you the
  budget. Knowing *which* questions can move to the cheap path without a user noticing
  — and which genuinely can't — is the skill.
- **Honesty about what you cut.** Every move to stay in budget gives something up.
  Naming the loss, and showing it's one a FinOps user won't feel, is the whole game —
  silent degradation that a customer *does* feel is the worst outcome.

## Deliverables

1. **A measured cost/latency picture** of your intelligence layer as it stands — real
   numbers, not estimates where you can avoid it.
2. **The design changes** that keep it inside a stated budget at a stated larger scale,
   and the projection that shows it holding.
3. **A short, honest account** of what each change costs in flexibility or fidelity,
   and why those losses are acceptable (or where they aren't).

## What we're looking for

An engineer who turns "feels fine" into a number, reasons about cost and latency at a
scale they can't see directly, and trades flexibility for cost-performance with their
eyes open and their reasons stated. This is the flexibility-versus-cost-performance
tradeoff from the scenario, pushed until it has to be quantitative.

---

**References:** [scenario](../scenario.md) · [data contract](../data_contract.md). **With your submission:** an [understanding ledger](../understanding_ledger.md). See the [challenge overview](./README.md).
