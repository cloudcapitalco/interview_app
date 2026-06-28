"""
Cloud Capital — commitment economics service.

A small HTTP service the application calls to get the economics of a *proposed*
commitment. It wraps the calculations in `economics.py` behind three endpoints:

  GET  /proposal       the default proposed commitment the product is built around
  POST /impact         the commitment's hourly impact on usage (the savings detail)
  POST /cost-of-risk   the cost of risk for the commitment, in points
  GET|POST /economics  the headline: aggregate impact, cost of risk, and the split

The service is **sufficient as shipped** — you can build everything the challenges
ask for against it as it stands. It is also **yours to change**: the source is here,
and modifying it is in scope. Run it, use it, and decide for yourself whether it is
shaped the way your application needs.

Run it:
    cd service && uv run uvicorn app:app --reload --port 8000
"""
from __future__ import annotations
from fastapi import FastAPI
from pydantic import BaseModel
import economics
from economics import Proposal

app = FastAPI(title="Cloud Capital — commitment economics")

# The default proposed commitment the product is built around.
DEFAULT = Proposal(scope="AWS#Compute", commitment_per_hour=16.0,
                   term_months=12, payment_option="no_upfront")

# One connection with the eligible usage lines loaded. Each request computes against it.
_con = economics.connect()


class ProposalBody(BaseModel):
    scope: str = DEFAULT.scope
    commitment_per_hour: float = DEFAULT.commitment_per_hour
    term_months: int = DEFAULT.term_months
    payment_option: str = DEFAULT.payment_option

    def to_proposal(self) -> Proposal:
        return Proposal(self.scope, self.commitment_per_hour,
                        self.term_months, self.payment_option)


@app.get("/proposal")
def proposal():
    """The proposed commitment the customer is being shown."""
    p = DEFAULT
    return {
        "instrument": "compute_savings_plan",
        "scope": p.scope,
        "commitment_per_hour": p.commitment_per_hour,
        "term_months": p.term_months,
        "payment_option": p.payment_option,
        "guaranteed_savings_rate": economics.economics(_con, p)["customer_savings_rate"],
    }


@app.post("/impact")
def impact(body: ProposalBody):
    """Every hour of the proposed commitment's impact, line by line.

    One record per hour per eligible usage line, for the whole window.
    """
    rows = economics.impact_rows(_con, body.to_proposal())
    return {"rows": rows}


@app.post("/cost-of-risk")
def cost_of_risk(body: ProposalBody):
    """The cost of risk for the proposed commitment, in points."""
    return economics.cost_of_risk(_con, body.to_proposal())


@app.api_route("/economics", methods=["GET", "POST"])
def economics_endpoint(body: ProposalBody | None = None):
    """Aggregate impact, cost of risk, and the customer / reserve / profit split."""
    p = body.to_proposal() if body else DEFAULT
    return economics.economics(_con, p)
