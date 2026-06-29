# Cloud Capital — Application Challenges

A set of build challenges for the customer-facing surface of a cloud-cost product,

on top of a real (anonymized) AWS cost-and-usage dataset. You're expected to use AI

agents heavily — see [what we value](docs/understanding_debt.md) and the

[challenge overview](docs/challenges/README.md).

## What we're actually testing

You can hand each of these challenges to an agent and get something that runs. That's

fine — it's the point. So the thing that distinguishes one submission from another is

**not** whether you got an agent to produce a working app. It's the **taste and**

**judgment you brought to it**: the architecture you chose, the UX calls you made, the

performance tradeoffs you reasoned through, and — above all — whether you *used what*

*you built*, noticed where it was subtly wrong or misleading or slow, and pushed back.

An agent left alone will happily build the plausible thing. A lot of the signal here

is in the gap between *plausible* and *right* — the misleading chart it didn't know

was misleading, the query that's fine on a sample and melts at scale, the screen that

flatters the product at the customer's expense. We're looking for the engineer who

catches those. **Plan to spend roughly as much of your time testing, feeling, and**

**correcting what you built as you spend generating it.**

Your user is a non-technical FinOps or finance owner. Build for them.

## Pick your stack

There is no required stack — front end, back end, datastore, and how you talk to an

LLM are all yours to choose, and the choice is itself signal. Pick something you can

move fast in *and* defend.

## The data and the service

The data is **not distributed with this repository** — it is provided separately.

Place the files in the `data/` directory (where the challenges, the data contract, and

the service expect them):

- `data/candidate_dataset.parquet` — the hourly cost-and-usage firehose
- `data/pricing_options_filtered.parquet` — the commitment pricing table

The **economics of a proposed commitment** don't come from a file — they come from a

small HTTP service that ships in [`service/`](service/README.md) and runs against the

data above. It's provided, sufficient as-is, and yours to change. Every field and

endpoint is described in the [data contract](docs/data_contract.md).

**Don't have the data?** Email [**engineering@cloudcapital.co**](mailto:engineering@cloudcapital.co) to request a

pre-signed download link (valid for one week).

## Where to go


|                                                              |                                                                                                                |
| ------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| [docs/scenario.md](docs/scenario.md)                         | The situation you're operating in, the users, and your standing permission to make calls. **Read this first.** |
| [docs/challenges/](docs/challenges/README.md)                | The challenges, a suggested order, and how the set is meant to be approached.                                  |
| [docs/data_contract.md](docs/data_contract.md)               | What's given to you — the usage firehose, the pricing table, and the economics service.                        |
| [service/README.md](service/README.md)                       | The provided economics service: how to run it, its endpoints, and that it's yours to change.                   |
| [docs/understanding_debt.md](docs/understanding_debt.md)     | What we value — read this before you start.                                                                    |
| [docs/understanding_ledger.md](docs/understanding_ledger.md) | The short ledger to submit with your work.                                                                     |


