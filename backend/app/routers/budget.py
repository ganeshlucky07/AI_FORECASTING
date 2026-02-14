from datetime import date
from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..utils import exporters

router = APIRouter()


@router.post("/upload_history", response_model=schemas.Message)
def upload_budget_history(
    payload: schemas.BudgetUploadRequest,
    db: Session = Depends(get_db),
):
    """
    Store historical budget data (revenue, expenses, workforce cost).
    """
    for rec in payload.records:
        row = models.BudgetHistory(
            date=rec.date,
            revenue=rec.revenue,
            expenses=rec.expenses,
            workforce_cost=rec.workforce_cost,
        )
        db.add(row)

    db.commit()
    return schemas.Message(message="Budget history uploaded successfully.")


@router.get("/forecast", response_model=schemas.BudgetForecastResponse)
def forecast_budget(
    horizon_months: int = 6,
    db: Session = Depends(get_db),
):
    """
    Very small "model" for budget forecasting.

    Approach:
    - Use the last available month (or average of all) as a baseline.
    - Project the same values forward for `horizon_months`.

    You can swap this out for:
    - Time series regression (e.g. ARIMA)
    - Multivariate models that include workforce plans & demand
    """
    rows: List[models.BudgetHistory] = (
        db.query(models.BudgetHistory)
        .order_by(models.BudgetHistory.date)
        .all()
    )

    if not rows:
        return schemas.BudgetForecastResponse(horizon_months=horizon_months, forecasts=[])

    # Simple baseline: average of all rows.
    avg_revenue = sum(r.revenue for r in rows) / len(rows)
    avg_expenses = sum(r.expenses for r in rows) / len(rows)
    avg_workforce_cost = sum(r.workforce_cost for r in rows) / len(rows)

    last_date: date = rows[-1].date
    forecasts: List[schemas.BudgetForecastPoint] = []

    # Assume data is monthly; in a real system you'd use pandas/relativedelta.
    year = last_date.year
    month = last_date.month
    for _ in range(horizon_months):
        # Move to next month.
        month += 1
        if month > 12:
            month = 1
            year += 1
        target_date = date(year, month, 1)

        forecasts.append(
            schemas.BudgetForecastPoint(
                date=target_date,
                projected_revenue=avg_revenue,
                projected_expenses=avg_expenses,
                projected_workforce_cost=avg_workforce_cost,
            )
        )

    return schemas.BudgetForecastResponse(
        horizon_months=horizon_months,
        forecasts=forecasts,
    )


@router.get("/export/excel")
def export_budget_forecast_excel(
    horizon_months: int = 6,
    db: Session = Depends(get_db),
):
    """
    Export the projected budget to an Excel file.
    """
    forecast = forecast_budget(horizon_months=horizon_months, db=db)

    rows = [
        {
            "date": point.date,
            "projected_revenue": point.projected_revenue,
            "projected_expenses": point.projected_expenses,
            "projected_workforce_cost": point.projected_workforce_cost,
        }
        for point in forecast.forecasts
    ]

    output = exporters.rows_to_excel(
        rows,
        columns=[
            "date",
            "projected_revenue",
            "projected_expenses",
            "projected_workforce_cost",
        ],
    )

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": 'attachment; filename="budget_forecast.xlsx"'},
    )

