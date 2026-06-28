# Challenge: Stand up the surface

## Scenario

Before anything is explorable, a customer has to land somewhere and immediately get
the point. They open the product, see the commitment we're proposing, and — in the
first thirty seconds, knowing nothing about the data model — understand **what it
saves them.** This challenge is that landing, and the architecture underneath it that
everything else hangs from.

## The task

Consume the [data contract](../data_contract.md) and stand up the surface: a running
front end and back end that pull the proposed commitment and its economics from the
[economics service](../../service/README.md) (`/proposal`, `/economics`) and present
the **headline** honestly — what's being proposed, and the savings it produces against
this customer's real usage.

This is the orienting challenge. Most of its value is in the **shape** you choose:
how the back end reads and serves the data, how the front end is structured, where
the boundary between them sits. You will be living in these decisions for every
challenge after this one, so make them on purpose.

## What makes it non-trivial

- **The headline must be honest.** `net_savings` is signed — under-utilized hours
  produce *negative* savings, and `wasted_commitment` is real. A headline that quotes
  gross savings and hides the waste is the kind of thing this whole product exists to
  *not* do. Decide what the honest single number is, and show it.
- **The data layer is a real choice, not a default.** The firehose is large. Even the
  headline is an aggregate over it. How you load, shape, and serve that — and where
  you draw the line between precomputed and on-demand — is the first instance of a
  decision you'll make repeatedly.

## Deliverables

1. **A running surface** — front end and back end — that loads the contract and shows
   the proposal and an honest headline savings figure.
2. **The architectural skeleton** the rest of the build hangs from: how data flows
   from the contract through the back end to the screen.
3. **A short note** on the shape you chose and why — the calls that will be expensive
   to change later.

## What we're looking for

The instinct to set up a structure a teammate could extend without a tour guide, and
the judgment to show a customer the *true* number on the first screen rather than the
flattering one. We care more about the shape and the honesty here than about how much
is on the screen.

---

**References:** [scenario](../scenario.md) · [data contract](../data_contract.md). **With your submission:** an [understanding ledger](../understanding_ledger.md). See the [challenge overview](./README.md).
