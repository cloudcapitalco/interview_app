# The challenges

A set of build challenges for the customer-facing surface described in
[the scenario](../scenario.md). Read the scenario and the
[data contract](../data_contract.md) first — the challenges assume both.

## Read these first

- [The scenario](../scenario.md) — the situation, the users, and your standing permission to make calls.
- [The data contract](../data_contract.md) — what's given to you (the usage firehose, the pricing table, and the **economics service**) and what you must *not* reimplement.
- [The economics service](../../service/README.md) — the running service that hands you a proposed commitment's economics. Provided, sufficient, and yours to change.
- [What we value: understanding over output](../understanding_debt.md).
- [The understanding ledger](../understanding_ledger.md) — submit one with your work.

## This is deliberately bigger than one person can build by hand

The full set describes more product than anyone could carefully build unaided in the
time given — you are **expected to use AI agents heavily.** It is very likely scaled
past what you can build *and* fully understand. **That tension is the point:** you
will trade off **how much you ship** against **how much of it you genuinely
understand and could defend** — the same bet an engineering lead makes delegating to
a team.

**Plan to spend up to about 3 hours.** There is **no target completion level — we are
not counting features, and we do not expect you to finish the set.** Success looks
like: **a meaningful, working surface, for a reasonable investment of time, whose
shape you architected and can defend.** We would far rather see two challenges whose
architecture you own than five you stapled together from agent output and can't walk
us through. Use AI to go fast and wide; choose where to go deep; be honest in your
[understanding ledger](../understanding_ledger.md) about which is which.

You choose the stack. You may scope down any challenge — a smaller surface you fully
own beats a sprawling one you can't.

## Suggested order

It builds naturally — each step leans on the ones before it. The center of gravity
is challenge 4; the first three get you to the point where it's worth doing well.

1. [Stand up the surface](./stand_up_the_surface.md) — consume the contract, show the headline, set the architecture.
2. [Explore the spend](./explore_the_spend.md) — the explorer core: slice the firehose, fluidly, over real volume.
3. [The honest split](./the_honest_split.md) — show what we keep, and turn a vendor's margin into trust instead of alarm.
4. [Ask and explain](./ask_and_explain.md) — the intelligence layer, and the throughput-vs-cost decision at the heart of this interview *(the centerpiece)*.
5. [The cost budget](./the_cost_budget.md) — make that decision quantitative, under an explicit budget and at scale *(hard)*.

[The misleading view](./the_misleading_view.md) is a short, anytime probe — pick it
up whenever a screen you built could mislead a customer who trusted it.

## What to submit

Package your work as a git repository or a zip and send it back through the same
contact who sent you this challenge. Please include:

- **The running surface** — source we can build and run, with whatever seed/setup it
  needs, plus a short note on how to start it and what to look at.
- **A short architecture note** — the shape of what you built and *why*: the data
  layer, where the LLM sits, the boundaries, the calls you made and the ones you
  delegated. A page is plenty.
- **An [understanding ledger](../understanding_ledger.md)** — what you genuinely
  understand versus what you leaned on AI for. Read [what we value](../understanding_debt.md)
  first; this is the part we weigh most, and we will probe it.

Make it something we can re-run and that you can walk us through and defend in a
follow-up conversation.
