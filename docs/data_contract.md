# The data contract

This is what the data team hands you. You consume it; you don't compute it. The
**sizing of the commitment, the savings it generates, and the reserve/profit split
are all already calculated** — they arrive as the tables below. Your job is to make
them explorable, legible, and trustworthy. (If you find yourself reimplementing the
commitment math, stop — that's not this interview. See [the scenario](./scenario.md).)

Two kinds of thing are provided: **static data** in [`../data`](../data) (the usage
firehose you let customers explore, and the pricing table behind it), and a running
**economics service** in [`../service`](../service) that hands you the given economics
of a proposed commitment laid over that usage.

---

## 1. The usage firehose — `data/candidate_dataset.parquet`

The customer's normalized hourly cost-and-usage data — the substrate the customer
explores and verifies against. One row per hour per usage line (a distinct
combination of the dimension columns), measures summed within that combination.
It is **anonymized real data** — shapes, distributions, and relationships are
genuine — spanning multiple linked AWS accounts (~22M rows, ~12 months of hourly
data). It is large; treat it as unbounded.

A few properties of real billing data that are worth knowing before you present it —
they are easy to get subtly wrong:

- **The most recent `billing_period` is partial.** The data cuts off mid-day on the
  last day available, so the final month has far fewer hours than a full one. A
  month-over-month view that treats it as complete will imply a cliff that isn't real.
- **`timestamp` is UTC.** Hour-of-day and day boundaries shift if you bucket in
  another zone.
- **Dimensions are high-cardinality and sparse.** `usage_type` has well over a
  thousand distinct values; `instance_type` and `commitment_key` are **null on the
  large majority of rows** (most spend is requests, data transfer, storage — things
  with no instance or commitment dimension). A breakdown by one of these has to decide,
  honestly, what to do with the null majority and the long tail.
- **Unit rates span many orders of magnitude.** `on_demand_cost / usage_amount`
  ranges from tens of dollars to small fractions of a cent depending on `usage_type`,
  and some rows are genuinely \$0.

| Column | Type | Definition |
|---|---|---|
| `timestamp` | timestamp | Start of the metered hour (UTC). |
| `billing_period` | string | AWS monthly billing period, `YYYY-MM`. |
| `product_code` | string | AWS service code (`AmazonEC2`, `AmazonECS` for Fargate, `AWSLambda`, `AmazonRDS`, …). 64 distinct. |
| `usage_type` | string | Region-prefixed AWS usage-type string (e.g. `EUC1-Fargate-vCPU-Hours:perCPU`). The prefix encodes the region. ~1,300 distinct. |
| `instance_type` | string (nullable) | Instance/resource type for instance-based usage (e.g. `m5.xlarge`); **null for usage with no instance dimension** (the majority). |
| `account_id` | string | Anonymized AWS account that incurred the usage (stable hash). A few dozen linked accounts. |
| `usage_amount` | double | Quantity in the native unit implied by `usage_type`. |
| `on_demand_cost` | double | Cost at public on-demand rates — no commitment applied. The unit rate is `on_demand_cost / usage_amount`. |
| `commitment_key` | string (nullable) | Hierarchical key describing the commitment scope of this usage; `None` when the usage is not commitment-eligible (the majority). The dimension along which commitments apply. |

> These are the dimensions a customer slices by. The file carries additional columns
> describing the customer's **existing** commitments (see the note below); the ones
> above are the dimensions and the on-demand baseline you build exploration on.

### Existing-commitment columns (context, not your subject)

The file also carries `amortized_cost`, `commitment`, `cost_type`, `baseline_covered`,
and `baseline_max`. These describe the customer's **already-active** commitments — what
they're paying today and where it differs from on-demand:

- `amortized_cost` — what this usage actually costs given existing commitments;
  differs from `on_demand_cost` wherever a commitment already applied.
- `cost_type` — `On Demand Usage`, `Usage with Discount` (covered by an existing
  commitment), `Unused Commitment` (committed capacity that went to waste), `Spot
  Usage`.
- `commitment`, `baseline_covered`, `baseline_max` — the covering instrument and the
  account's historical baseline coverage.

This is real context a customer might want to see — *today's* posture. But the product
this challenge is about is built around a **proposed** commitment, whose economics are
given to you separately in §2. Don't conflate the two, and don't try to reconstruct the
proposed savings from these existing-commitment columns — the proposal is a forward
overlay, not something in the historical bill.

---

## 2. The pricing table — `data/pricing_options_filtered.parquet`

The Savings-Plan / Reserved-Instance rate table, filtered to the instruments and
regions in the dataset. You will not generally touch this directly — it is the input
the economics service uses to price a commitment — but it's here for reference and so
the service can run. Key columns: `price_list_key` (joins to the firehose),
`instrument_type`, `term_months`, `payment_option`, `rate`, `unit`, `currency`.

---

## 3. The given economics — the **economics service**

The **proposed** commitment's economics are not a file — they come from a small HTTP
**service** that ships in [`../service`](../service) (run instructions there). This is
the forward overlay: it is not in the historical bill, and you do not compute it. You
**call the service** and present what it returns. The split is given; the math is
settled.

The service answers for any proposed commitment:

- **`/proposal`** — the default proposed commitment the product is built around (a
  Compute Savings Plan over `AWS#Compute`).
- **`/impact`** — the commitment's impact, **one record per hour per eligible usage
  line** for the whole window: `covered_on_demand_cost`, `committed_cost`, and
  `gross_savings` (`covered_on_demand_cost − committed_cost`). This is the savings
  detail your exploration surface rolls up.
- **`/cost-of-risk`** — the cost of risk in points (4–80), with the `protection` and
  `trend` behind it. A stand-in for our proprietary risk model.
- **`/economics`** — the headline: aggregate impact plus the split. Of the net savings
  the commitment generates, **profit is a fixed 10%**, the **reserve is the
  cost-of-risk points**, and the **customer keeps the rest** as their guaranteed share.
  (`net_savings = customer_savings + reserve + profit`.)

Two things to keep in mind as you build on it:

- **`net_savings` is signed.** Over-committing produces under-utilized hours where
  `wasted_commitment` exceeds the gross saving and net savings go *negative*. A view
  that shows only the positive part, or quotes `gross_savings` as "savings," is telling
  the customer something untrue. The distribution of per-hour savings is **not
  symmetric**; summary stats that assume it is will mislead.
- **The service is provided, sufficient, and yours to change.** It will answer
  everything the challenges need as it stands. Its source is in the repo, and modifying
  it is in scope. Whether the way it hands you data is the way your application wants to
  receive it is a question worth forming your own opinion on.

---

> **A note on scale.** What ships here is one customer's data and one proposal. The
> product is not. Design as if a row count and a customer count an order of magnitude or
> two larger are coming — because in [The cost budget](./challenges/the_cost_budget.md)
> they are.
