# Challenge: Ask and explain

> The centerpiece. The decision you make here is the one we are most interested in.

## Scenario

The customer is not an engineer, and the most natural thing they can do is *ask.*
"Why is the saving smaller for that account?" "What's driving the spend this
commitment covers?" "What changed since last month?" And between visits, they'd value
a short, plain-language feed that **narrates** what moved — the proposal and its
performance, in words they understand. This is the layer that turns a data-rich
surface into something a layperson can actually hold.

## The task

Build the intelligence layer: a natural-language **ask** (question in, the right view
and a trustworthy short explanation out) and a **narration** feed of what changed.
Make it feel intelligent — and make it something you could actually run in production
for every customer, on every question, without it bankrupting the company or making a
finance user wait.

## The decision this is really about

There is an obvious implementation — point a large language model at the data and let
it answer — and it is a trap. The data is a [firehose](../data_contract.md). If every
question and every line of narration pushes raw volume through a model, you get a demo
that dazzles and a product that is **ruinous in production**: cost that scales with the
size of the customer's bill, and latency that makes the thing feel broken. At the
other extreme, you pre-bake every view and template every sentence — cheap, instant,
and unable to answer the question you didn't anticipate.

**The whole challenge is finding the right point between those, and defending it.**
The key realization is that the answer is already in your build: the
**aggregation/query layer from [Explore the spend](./explore_the_spend.md) is the
low-throughput, structured surface you hand the model instead of the firehose.** The
model reasons and explains over bounded, pre-shaped results — it orchestrates the
query layer; it never touches a million rows. (The same question applies one layer
down: the [economics service](../../service/README.md) hands *you* a firehose too —
whether that's the right boundary, or whether it should hand back something already
collapsed, is yours to decide.) Around that sit the levers you actually have:

- **Where the boundary is** — what the model is allowed to see and call, and what it
  is structurally prevented from doing (raw-row access, unbounded scans).
- **What you collapse before the model** — aggregation, a constrained query/tool
  interface, classification of the question, templating the common cases, caching,
  routing only the genuinely novel question to the expensive path.
- **What you spend flexibility on, on purpose** — the open-ended questions where a
  template would fail and the model's generality is worth the cost and the latency.

We want to watch you **reason explicitly about flexibility versus cost and
performance** — name what you give up when you compress the stream, decide whether a
FinOps user would ever notice that loss, and make the call. There is no single right
answer. There is an enormous difference between a thoughtful answer and a naive one.

## Trust boundary

The model is talking to a customer about their money. Numbers it states must be
*true* — grounded in the given data, not generated. Decide how you keep the model from
inventing figures, and how a user can tell what's computed from what's narrated. An
explanation that sounds confident and is wrong is worse here than no explanation.

## Deliverables

1. **The working ask + narration** over your data, end to end.
2. **The architecture of the boundary** — where the model sits relative to your query
   layer, what it can and cannot reach, and how you keep its numbers grounded.
3. **A written defense of the tradeoff** — the throughput/cost/latency/flexibility call
   you made, what each choice buys and costs, where you'd land differently if cost
   mattered more, or latency, or flexibility. This write-up matters as much as the
   feature.

## What we're looking for

The judgment to spend an LLM's flexibility where it pays for itself and engineer it
away where it doesn't, a trust boundary you designed rather than hoped for, and the
ability to defend the whole thing as a deliberate set of tradeoffs. This is the
secondary thing this interview exists to test, made concrete.

---

**References:** [scenario](../scenario.md) · [data contract](../data_contract.md). **With your submission:** an [understanding ledger](../understanding_ledger.md). See the [challenge overview](./README.md).
