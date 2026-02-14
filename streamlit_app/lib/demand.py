"""Demand forecasting logic (moving average) for Streamlit app. Uses pandas, no DB."""
from datetime import date, timedelta
from typing import Dict, List

import pandas as pd


def forecast_demand(
    df: pd.DataFrame,
    horizon_days: int = 30,
    window: int = 7,
) -> List[Dict]:
    """
    Simple moving-average demand forecast from a DataFrame with columns:
    product_name, date, quantity.
    Returns a flat list of { product_name, date, predicted_quantity }.
    """
    if df is None or df.empty or "product_name" not in df.columns or "quantity" not in df.columns:
        return []
    if "date" not in df.columns:
        return []
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"]).dt.date
    today = date.today()
    out = []
    for product_name, g in df.groupby("product_name"):
        qty = g.sort_values("date")["quantity"].tail(window)
        if qty.empty:
            continue
        avg = float(qty.mean())
        for i in range(1, horizon_days + 1):
            d = today + timedelta(days=i)
            out.append({"product_name": product_name, "date": d, "predicted_quantity": avg})
    return out
