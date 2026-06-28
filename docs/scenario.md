# The scenario

> Read this first. It sets the situation you're operating inside, the users you're
> building for, and the standing permission you have to make judgment calls. The
> individual challenges assume you've internalized it.

## Where you've landed

You've just joined **Cloud Capital** as an application engineer. Cloud Capital helps
companies spend less on cloud. We ingest a customer's cloud cost-and-usage data and
manage their **commitments** — Savings Plans and Reserved-Instance–style instruments
where someone promises AWS a fixed hourly spend for a term in exchange for a
discount.

The thing that makes us unusual is **where the risk sits.** We don't hand a customer
a recommendation and wish them luck. We **guarantee them a savings rate**, and then
we carry the risk of hitting it ourselves. When our commitments overperform the
guarantee, we keep the difference — that's our profit, and it feeds a shared risk
pool. When they underperform, we pay the difference out of our own bottom line. The
customer gets a clean, guaranteed number; we live or die on whether we sized the
bet right.

We compete against other optimization providers, and many of them get their edge by
mitigating risk through tactics AWS doesn't sanction. We don't — we operate inside
the rules. What keeps us competitive anyway is discipline and honesty about the math:
a customer has a reasonable **baseline** for the savings they ought to expect, and we
hold back a reserve and a profit margin calibrated to that baseline and to what the
risk genuinely requires — no more. Operating cleanly, our reserve and margin still
land where we can out-compete the less scrupulous. Our real edge is that, because the
deal is honest, **we can show it to the customer** — the savings, the risk, the
split, all of it. The sneaky players can't. The product surface that does the showing
— the one the customer lives in — is **yours.**

## The product you own

You own the customer-facing surface where a customer **sees a commitment we're
proposing, understands the savings it actually generates against their own usage, and
sees — honestly — the split between what they keep and what we hold back** as risk
reserve and profit. It's a cost-explorer-like surface, but pointed at a purpose:
turning our proposal into something a customer can interrogate, verify against their
real bill, and *trust*.

The raw material is a normalized cost-and-usage dataset: hourly line items across a
customer's whole footprint — service, region, account, instance type, usage type,
and the commitment coverage on each row — clean, and **large.** A proposed
commitment, and the savings it produces against that usage, are **given to you** —
the sizing of the bet and the calibration of the reserve happen elsewhere in the
company and are not part of this. Your craft is the part the customer touches: the
front end that turns a dense, data-rich picture into something legible, and the back
end that can answer an analytical question over a firehose fast enough that exploring
feels like thinking.

You are **not** doing data science. You are not sizing commitments, building
forecasts, or modeling risk. You are building the surface that makes a given proposal
and its real economics explorable and trustworthy — which is data **visualization**
and the data **manipulation** underneath it, not statistics.

## Who you're building for

Your user is not an engineer. Picture the **FinOps lead or the platform/finance
owner** at a company spending somewhere between one and tens of millions of dollars
a year on AWS. They are smart, busy, accountable for real money, and not going to
read a SQL query. They open your product to do three things:

1. **Understand the offer at a glance.** What are we proposing, and what does it save
   them — the guaranteed number, plainly, in the first thirty seconds, no expertise
   required.
2. **See how it lands on their real usage, and verify it.** Slice the underlying
   cost-and-usage data by any dimension they think in — service, team, region,
   environment, tag — and follow the savings down to where they actually come from,
   so the proposal checks out against the bill they already know.
3. **Understand the deal honestly — including the split.** What they keep versus what
   we hold back as reserve and profit, why that split is what it is, and the nature of
   the risk we're carrying on their behalf. This is the transparency our competitors
   can't offer, made concrete.

The phrase to keep in your head is **progressive mastery.** A first-time visitor
should get a clear "so what" immediately, understanding none of the domain. The same
person, ninety days later, should drive the same surfaces like an analyst — pivoting,
drilling, comparing, interrogating a number — and never hit a wall where the product
stops explaining itself. You are designing a tool someone *grows into*, not a
dashboard they bounce off of or a cockpit they can't fly.

## The firehose, and the data work underneath the pictures

The surface is only as good as the data layer beneath it. The usage dataset is a
**firehose** — hourly line items across thousands of resources, millions of rows,
unbounded and growing. Every view the customer wants is some aggregation over that
volume: a savings trend is a time rollup, "where do the savings come from" is a
group-by over a high-cardinality dimension, "what changed" is a top-N delta between
two windows. Making those feel instant — deciding what to pre-aggregate, what to
compute on demand, how to keep an interactive surface responsive over real volume —
is a substantial back-end design problem, and it is squarely application engineering,
not statistics.

Hold onto that aggregation layer. It is about to do double duty.

## The intelligence layer (and the tradeoff at the center of this interview)

Cloud Capital wants the surface to feel **intelligent**, not just interactive. The
ambition is a layer that lets a non-technical user **ask in plain language and get a
trustworthy answer** — the right chart, the right breakdown, and a short explanation
— "why is the proposed saving smaller for that account?", "what's driving the spend
this commitment covers?", "what changed since last month?" — plus a feed that
**narrates** the proposal and its performance in words they understand.

The obvious way to build that is to point a large language model at the data and let
it rip. And here is the problem you cannot design your way around: the data is the
firehose above. If every question and every explanation pushes raw volume through an
LLM, you get something that dazzles in a demo and is **ruinous in production** — the
cost scales with the size of the customer's bill, and the latency makes a finance
user feel the product is broken. At the other extreme, you pre-bake every view and
template every sentence: cheap, fast, and unable to answer the question you didn't
anticipate.

**The real work is in between, and finding the right point on that line is the heart
of this interview.** Notice that the answer is hiding in the data layer you already
built: the aggregation and query interface that makes visualization fast is *exactly*
the **low-throughput, structured surface you can hand the LLM instead of the
firehose.** The model orchestrates and explains over bounded, pre-shaped results; it
never touches a million rows. Where do you collapse the stream that way — with
aggregation, a constrained query interface, templating, caching, and routing — and
where do you genuinely spend the model's open-ended flexibility, and the cost and
latency that come with it, on purpose? What do you give up when you compress the
stream, and is that a loss a FinOps user will ever notice? We want to watch you
**reason explicitly about flexibility versus cost and performance**, make the call,
and defend it. There is no single right answer — but there is a great deal of
distance between a thoughtful answer and a naive one.

## The standard you're held to

You will be asked to build more than one person can carefully build by hand in the
time given. That is deliberate: you are expected to use AI agents heavily, to
produce far more than you could alone — and the thing we are actually evaluating is
whether you stay the person who **understands** what you shipped.

It is very easy, with agents, to generate a working app whose architecture you can't
defend, whose trust boundaries you haven't thought about, and whose behavior under
real load you can't predict. That is **understanding debt** — the gap between how
much product exists and how much of it you genuinely comprehend — and it comes due
the moment something breaks or a real decision has to be made. (Read
[what we value](./understanding_debt.md); it's the lens we grade through.)

We are **not** holding you to "I wrote every line" — no one delegating well can
claim that, and we don't want you to. The bar is the one a strong engineering lead is
actually held to: **you architected the shape of this.** You chose the structure and
can say why; you understand how the pieces fit and where the boundaries are — the
data model, the query layer, the trust boundary around the LLM, that
throughput-versus-cost call; you can explain and defend any part of it, and you could
redirect it. Push the boilerplate, the wiring, and the styling to your agents. Keep
your head on the decisions that give the system its shape, and on the moments of the
experience that earn or lose a customer's trust.

Concretely, the work is judged on the taste a senior application engineer is hired
for:

- **Architecture that scales** — front end and back end — that a teammate could
  extend without a tour guide.
- **Maintainable code** you can stand behind, not a pile an agent emitted that
  happens to run.
- **User experience** that delivers the *progressive mastery* above: honest with
  data, legible to a layperson, deep enough for an analyst.
- **Judgment about the LLM** — spending its flexibility where it pays for itself and
  engineering it away where it doesn't.

## You have permission

This is a scenario, and inside it you are the engineer who owns the product. Where a
challenge leaves something unspecified, **you may make the call** — choose the
stack, the framing, the scope you go deep on — as long as you can explain why. We'd
far rather see a smaller surface you fully own and can defend than a sprawling one
you can't. Decide where to go deep, delegate the rest, and be honest about which is
which.
