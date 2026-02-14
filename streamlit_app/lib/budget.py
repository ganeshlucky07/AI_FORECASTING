"""Budget projection logic for Streamlit app."""
from datetime import date
from typing import List

import pandas as pd


def forecast_budget(
    df_revenue_expenses,
    horizon_months: int = 6,
) -> List[dict]:
    """
    Simple average-based budget forecast.
    df_revenue_expenses must have columns: date, revenue, expenses, workforce_cost.
    Returns list of { date, projected_revenue, projected_expenses, projected_workforce_cost }.
    """
    if df_revenue_expenses is None or df_revenue_expenses.empty:
        return []
    needed = ["date", "revenue", "expenses", "workforce_cost"]
    if not all(c in df_revenue_expenses.columns for c in needed):
        return []
    df = df_revenue_expenses.copy()
    df["date"] = pd.to_datetime(df["date"])
    avg = df[["revenue", "expenses", "workforce_cost"]].mean()
    last = df["date"].max().date() if hasattr(df["date"].max(), "date") else df["date"].max()
    if hasattr(last, "year"):
        year, month = last.year, last.month
    else:
        year, month = 2024, 1
    out = []
    for _ in range(horizon_months):
        month += 1
        if month > 12:
            month = 1
            year += 1
        d = date(year, month, 1)
        out.append({
            "date": d,
            "projected_revenue": float(avg["revenue"]),
            "projected_expenses": float(avg["expenses"]),
            "projected_workforce_cost": float(avg["workforce_cost"]),
        })
    return out
