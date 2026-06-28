# Challenge: Explore the spend

## Scenario

The headline earns a glance; it doesn't earn trust. Trust comes when the customer can
**take the number apart** — slice their own spend the way they think about their
business, follow the savings down to where they actually come from, and find that the
proposal checks out against the bill they already know. This is the explorer at the
core of the product.

## The task

Build the exploration surface: let the customer slice the usage firehose and the
commitment's savings across the dimensions they care about — service (`product_code`),
account, region and usage kind (`usage_type`), instance type, commitment scope —
compare periods, and drill from a total down to the handful of usage lines driving it.
It should feel like *thinking*: a question, then the answer, fast enough that the next
question is already forming.

## What makes it non-trivial

This is the **data-manipulation-for-visualization** challenge, and it is squarely
back-end engineering, not statistics:

- **Every view is an aggregation over volume.** A trend is a time rollup; a breakdown
  is a group-by over a high-cardinality, sparse dimension (`usage_type` has well over a
  thousand values; `instance_type` is null on most rows); "what drove this" is a top-N
  delta between two windows. Doing those interactively, over ~22M rows, without the
  surface feeling broken, is the problem.
- **What do you precompute, and what do you compute on demand?** You cannot
  pre-aggregate every cut — the dimension combinations explode. You also cannot scan
  the firehose on every interaction. Where you draw that line *is* the challenge, and
  the structure you land on here is the one the LLM will lean on in challenge 4 — so
  build it like an interface, not a one-off.
- **Where do the savings come from?** The commitment's savings detail comes from the
  [economics service](../../service/README.md)'s `/impact`. Look at what it actually
  returns before you design around it — its shape will shape yours, unless you decide
  otherwise.
- **Progressive mastery.** A first-time user needs a sensible default view and a path
  in; an analyst needs to pivot and drill without hitting a wall. The same surface has
  to serve both.

## Deliverables

1. **The exploration surface** — slice, compare, and drill across dimensions, with the
   savings rolling up correctly under every cut.
2. **The query/aggregation layer** beneath it, designed as a reusable interface — the
   thing that answers "spend and savings, grouped this way, filtered that way, over
   this window."
3. **A short note** on your precompute-vs-on-demand line and how it holds up as volume
   grows.

## What we're looking for

A back end whose aggregation layer is clean enough to reuse and fast enough to make
exploration feel fluid, and a front end that lets a layperson start simple and an
analyst go deep on the same screen. Be ready to explain where your design would strain
as the data grows, and what you'd do about it.

---

**References:** [scenario](../scenario.md) · [data contract](../data_contract.md). **With your submission:** an [understanding ledger](../understanding_ledger.md). See the [challenge overview](./README.md).
