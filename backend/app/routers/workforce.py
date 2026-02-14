from datetime import timedelta
from math import ceil
from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..utils import exporters

router = APIRouter()


@router.post("/plan", response_model=schemas.WorkforcePlanResponse)
def generate_workforce_plan(
    request: schemas.WorkforcePlanRequest,
    db: Session = Depends(get_db),
):
    """
    Very simple workforce planning engine.

    Idea:
    - Assume a constant predicted_daily_demand over the period.
    - Each employee can handle `productivity_per_employee` units per day.
    - Required headcount = ceil(demand / productivity).
    - Save and return a plan entry per day in the requested range.

    This is deliberately simple to keep the example clear. You can
    replace it with a more advanced linear programming / optimization
    model (e.g., using PuLP or OR-Tools).
    """
    plans: List[schemas.WorkforcePlanEntry] = []

    current = request.start_date
    while current <= request.end_date:
        required = ceil(
            request.predicted_daily_demand / request.productivity_per_employee
        )

        # Persist a basic workforce plan row.
        plan_row = models.WorkforcePlan(
            date=current,
            department=request.department,
            required_headcount=required,
        )
        db.add(plan_row)

        plans.append(
            schemas.WorkforcePlanEntry(
                date=current,
                department=request.department,
                required_headcount=required,
            )
        )

        current += timedelta(days=1)

    db.commit()
    return schemas.WorkforcePlanResponse(plans=plans)


@router.get("/export/excel")
def export_workforce_plans_excel(
    db: Session = Depends(get_db),
):
    """
    Export all stored workforce plans as an Excel file.

    This gives managers a way to archive or share staffing plans.
    """
    rows = (
        db.query(models.WorkforcePlan)
        .order_by(models.WorkforcePlan.date, models.WorkforcePlan.department)
        .all()
    )

    data = [
        {
            "date": r.date,
            "department": r.department,
            "required_headcount": r.required_headcount,
        }
        for r in rows
    ]

    output = exporters.rows_to_excel(
        data,
        columns=["date", "department", "required_headcount"],
    )

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": 'attachment; filename="workforce_plans.xlsx"'},
    )

