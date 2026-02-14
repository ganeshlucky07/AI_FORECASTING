"""Workforce planning logic for Streamlit app."""
from datetime import timedelta
from math import ceil
from typing import List


def plan_workforce(
    department: str,
    start_date,
    end_date,
    predicted_daily_demand: float,
    productivity_per_employee: float = 10.0,
) -> List[dict]:
    """Generate required headcount per day. Returns list of { date, department, required_headcount }."""
    plans = []
    current = start_date
    required = ceil(predicted_daily_demand / productivity_per_employee)
    while current <= end_date:
        plans.append({
            "date": current,
            "department": department,
            "required_headcount": required,
        })
        current += timedelta(days=1)
    return plans
