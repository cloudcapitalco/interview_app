# The commitment economics service

A small HTTP service the application calls to get the economics of a **proposed**
commitment, computed from the usage data and the pricing table in [`../data`](../data).
It is the source of the savings numbers your product presents.

**It is provided, and it is yours.** The service is sufficient as shipped — you can
build everything the challenges ask for against it as it stands. The source is right
here (`economics.py`, `app.py`), and **changing it is in scope.** Run it, build
against it, and decide for yourself whether it is shaped the way your application
needs it to be.

## Run it

The data files must be present in [`../data`](../data) (`usage.parquet` and
`pricing_options_filtered.parquet`). Then, from this directory:

```sh
uv sync
uv run uvicorn app:app --port 8000
```

The service loads the usage data once at startup, then answers requests against it.

## Endpoints

| Method | Path | What it returns |
|---|---|---|
| `GET` | `/proposal` | The default proposed commitment the product is built around. |
| `POST` | `/impact` | The commitment's impact on usage — one record per hour per eligible usage line, for the whole window. |
| `POST` | `/cost-of-risk` | The cost of risk for the commitment, in points (4–80), with the protection and trend it's based on. |
| `GET`/`POST` | `/economics` | The headline: aggregate impact, cost of risk, and the customer / reserve / profit split. |

`POST` bodies describe a proposed commitment (all fields optional; omitted fields fall
back to the default):

```json
{ "scope": "AWS#Compute", "commitment_per_hour": 16.0, "term_months": 12, "payment_option": "no_upfront" }
```

### How the economics fit together

- **Impact** — each hour, the committed discounted-dollar budget is allocated to that
  hour's eligible usage in order of decreasing discount (highest-discount usage
  covered first), use-it-or-lose-it. `covered_on_demand_cost − committed_cost` is the
  gross saving; budget paid but unused in an hour is `wasted_commitment`; net saving is
  gross minus waste, and **can be negative** when a level is over-committed.
- **Cost of risk** — a points figure (4–80) standing in for our proprietary risk
  model. It rises as the committed level is less *protected* by the usage above it and
  as usage *trends down*; it falls when the level sits comfortably below usage and
  usage is growing. At the top of the range the commitment is effectively infeasible.
- **The split** — of the net savings the commitment generates, profit is a fixed 10%,
  the reserve is the cost-of-risk points, and the customer keeps the rest as their
  guaranteed share.

> The numbers and the math are settled — you don't need to re-derive them. What you do
> with the service is the open question.
