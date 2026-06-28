"""
Commitment economics — the core calculations behind the two services.

Given a *proposed* commitment (a Compute Savings Plan at some hourly level), this
module computes:

  - its hourly impact on the customer's usage (what it covers, costs, saves, wastes),
  - a *cost of risk* for the commitment (a stand-in for our proprietary risk model),
  - the split of the savings into customer / reserve / profit.

These are the numbers the application presents. The math here is settled — you are
not expected to re-derive or change it to complete the challenges. The HTTP surface
in `app.py`, on the other hand, is fair game.
"""
from __future__ import annotations
import os
from dataclasses import dataclass, asdict
import duckdb

# Default to the repo's data/ directory regardless of where the service is launched from.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DATA = os.path.join(_REPO_ROOT, "data")
USAGE_PATH = os.environ.get("USAGE_PARQUET", os.path.join(_DATA, "usage.parquet"))
PRICING_PATH = os.environ.get("PRICING_PARQUET", os.path.join(_DATA, "pricing_options_filtered.parquet"))

# Profit is a fixed share of the savings the commitment generates.
PROFIT_RATE = 0.10
# Cost of risk is expressed in "points" (percent of generated savings held as reserve),
# bounded to this range. At the top of the range the deal is effectively infeasible.
COR_MIN_POINTS = 4.0
COR_MAX_POINTS = 80.0


@dataclass
class Proposal:
    scope: str = "AWS#Compute"          # commitment_key prefix a Compute SP covers
    commitment_per_hour: float = 16.0   # committed discounted $/hr
    term_months: int = 12               # 12 or 36
    payment_option: str = "no_upfront"


def connect() -> duckdb.DuckDBPyConnection:
    """A connection with the eligible Compute usage lines pre-loaded.

    Loading the source data once is cheap. Note what is *not* done here: nothing about
    a specific proposed commitment is precomputed or cached — every request recomputes
    its allocation from these lines (see `app.py`).
    """
    con = duckdb.connect()
    con.execute(
        f"""
        CREATE TABLE lines AS
        WITH elig AS (
          SELECT u.timestamp, u.account_id, u.product_code, u.usage_type,
                 u.instance_type, u.commitment_key, u.price_list_key,
                 u.on_demand_cost, u.usage_amount, p.rate AS sp_rate, p.term_months
          FROM '{USAGE_PATH}' u
          JOIN '{PRICING_PATH}' p
            ON u.price_list_key = p.price_list_key
           AND p.instrument_type = 'compute_savings_plan'
           AND p.payment_option = 'no_upfront'
          WHERE u.commitment_key LIKE 'AWS#Compute%'
            AND u.usage_amount > 0 AND u.on_demand_cost > 0
        )
        SELECT *,
          usage_amount * sp_rate AS line_disc_cost,           -- discounted $ to fully cover this line
          1 - sp_rate / (on_demand_cost / usage_amount) AS discount
        FROM elig
        WHERE 1 - sp_rate / (on_demand_cost / usage_amount) BETWEEN 0 AND 0.95
        """
    )
    return con


def _impact_relation(con, p: Proposal):
    """Per-line hourly impact of the proposed commitment, as an unmaterialized relation.

    Each hour, the committed discounted-dollar budget is allocated to that hour's
    eligible usage in order of decreasing discount (highest-discount usage covered
    first), use-it-or-lose-it.
    """
    L = float(p.commitment_per_hour)
    con.execute("CREATE OR REPLACE TEMP VIEW impact AS "
        f"""
        WITH ranked AS (
          SELECT timestamp, account_id, product_code, usage_type, instance_type,
                 commitment_key, on_demand_cost, line_disc_cost, discount,
                 SUM(line_disc_cost) OVER (PARTITION BY timestamp ORDER BY discount DESC
                     ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cum
          FROM lines
          WHERE term_months = {int(p.term_months)}
        )
        SELECT timestamp, account_id, product_code, usage_type, instance_type, commitment_key,
          GREATEST(0, LEAST(line_disc_cost, {L} - (cum - line_disc_cost))) AS committed_cost,
          CASE WHEN line_disc_cost > 0
               THEN GREATEST(0, LEAST(line_disc_cost, {L} - (cum - line_disc_cost))) / line_disc_cost
               ELSE 0 END * on_demand_cost AS covered_on_demand_cost
        FROM ranked
        """)
    con.execute("CREATE OR REPLACE TEMP VIEW impact_rows AS "
        """
        SELECT timestamp, account_id, product_code, usage_type, instance_type, commitment_key,
               covered_on_demand_cost, committed_cost,
               covered_on_demand_cost - committed_cost AS gross_savings
        FROM impact
        """)


def impact_rows(con, p: Proposal):
    """The full per-hour, per-usage-line impact. This is what `/impact` returns."""
    _impact_relation(con, p)
    cols = [c[0] for c in con.execute("DESCRIBE SELECT * FROM impact_rows").fetchall()]
    rows = con.execute("SELECT * FROM impact_rows").fetchall()
    return [dict(zip(cols, r)) for r in rows]


def _aggregate_economics(con, p: Proposal) -> dict:
    """Window-level totals for the proposed commitment (covered, committed, gross, waste, net)."""
    _impact_relation(con, p)
    L = float(p.commitment_per_hour)
    covered, committed, gross = con.execute(
        "SELECT sum(covered_on_demand_cost), sum(committed_cost), sum(gross_savings) FROM impact_rows"
    ).fetchone()
    # Waste is per hour: the committed budget paid but not consumed that hour.
    waste = con.execute(
        f"""WITH h AS (SELECT timestamp, sum(committed_cost) used FROM impact GROUP BY 1)
            SELECT sum(GREATEST(0, {L} - used)) FROM h"""
    ).fetchone()[0] or 0.0
    net = (gross or 0.0) - waste
    return {
        "covered_on_demand_cost": covered or 0.0,
        "committed_cost": committed or 0.0,
        "gross_savings": gross or 0.0,
        "wasted_commitment": waste,
        "net_savings": net,
    }


def cost_of_risk(con, p: Proposal) -> dict:
    """A plausible stand-in for our proprietary cost-of-risk model.

    Intuition: risk is high when the committed level is poorly *protected* by the
    usage sitting above it, and when usage is *trending down*; risk is low when the
    level is comfortably below typical usage and usage is *growing*.
    """
    _impact_relation(con, p)
    L = float(p.commitment_per_hour)

    # Protection: the fraction of hours whose eligible discounted spend covers the level.
    protection = con.execute(
        f"""WITH h AS (SELECT timestamp, sum(line_disc_cost) hr FROM lines
                       WHERE term_months = {int(p.term_months)} GROUP BY 1)
            SELECT avg(CASE WHEN hr >= {L} THEN 1.0 ELSE 0.0 END) FROM h"""
    ).fetchone()[0] or 0.0

    # Trend: normalized slope of eligible spend across *complete* months.
    trend = con.execute(
        f"""WITH m AS (
              SELECT billing_period_idx, total FROM (
                SELECT row_number() OVER (ORDER BY mo) AS billing_period_idx,
                       total, cnt
                FROM (
                  SELECT date_trunc('month', timestamp) mo, sum(line_disc_cost) total,
                         count(distinct timestamp) cnt
                  FROM lines WHERE term_months = {int(p.term_months)} GROUP BY 1
                )
              ) WHERE cnt >= 672   -- drop partial months (< 28 days of hours)
            )
            SELECT regr_slope(total, billing_period_idx) * count(*) / NULLIF(avg(total),0)
            FROM m"""
    ).fetchone()[0] or 0.0

    under = 1.0 - protection
    downtrend = max(0.0, -trend)
    uptrend = max(0.0, trend)
    # Poor protection drives risk; a downtrend amplifies it, an uptrend relieves it.
    combine = under * (0.6 + 0.8 * downtrend) + 0.4 * under ** 2 - 0.15 * uptrend * protection
    combine = min(1.0, max(0.0, combine))
    points = round(COR_MIN_POINTS + (COR_MAX_POINTS - COR_MIN_POINTS) * combine, 1)
    return {
        "cost_of_risk_points": points,
        "protection": round(protection, 3),
        "trend": round(trend, 3),
        "infeasible": points >= COR_MAX_POINTS,
    }


def economics(con, p: Proposal) -> dict:
    """The headline economics: aggregate impact, cost of risk, and the customer/reserve/profit split."""
    agg = _aggregate_economics(con, p)
    cor = cost_of_risk(con, p)
    S = agg["net_savings"]
    profit = PROFIT_RATE * S
    reserve = (cor["cost_of_risk_points"] / 100.0) * S
    customer_savings = S - profit - reserve
    return {
        "proposal": asdict(p),
        **agg,
        **cor,
        "profit": profit,
        "reserve": reserve,
        "customer_savings": customer_savings,
        "customer_savings_rate": (customer_savings / agg["covered_on_demand_cost"])
                                 if agg["covered_on_demand_cost"] else 0.0,
    }
