# Working in this repository (for agents)

This repository is a set of **application build challenges** for candidates: build the
customer-facing surface of a cloud-cost product on top of an anonymized AWS
cost-and-usage dataset. If you are an agent helping someone work through it, orient
yourself here.

**Start with [`README.md`](README.md)**, then [`docs/scenario.md`](docs/scenario.md) —
together they cover the situation, the user you're building for, where the data lives
(`data/`), and the standard the work is held to.

The stack is **not specified** — the candidate chooses the front end, back end,
datastore, and how the app talks to an LLM. If it isn't decided yet, ask; don't assume
a default. Stand up something runnable and keep it runnable.

Key references:

- [`docs/scenario.md`](docs/scenario.md) — the scenario: the product, the users, the central tradeoff. Internalize it before building.
- [`docs/challenges/README.md`](docs/challenges/README.md) — the challenges, a suggested order, and how the set is meant to be approached.
- [`docs/data_contract.md`](docs/data_contract.md) — every field of the given data: the usage firehose and the proposed commitment's economics. **The savings and the reserve/profit split are given — do not recompute the commitment math.**
- [`docs/understanding_debt.md`](docs/understanding_debt.md) and [`docs/understanding_ledger.md`](docs/understanding_ledger.md) — what the work is evaluated on. The candidate must be able to explain and defend the *shape* of what gets built, so surface your assumptions and decisions to them as you go rather than burying them.

A note on how this is graded: the candidate is being judged on taste and judgment —
UX calls, performance tradeoffs, and whether the result is honest with the customer —
not on feature count. Build real, working software, but flag the decisions that carry
those tradeoffs so the candidate can own them.
