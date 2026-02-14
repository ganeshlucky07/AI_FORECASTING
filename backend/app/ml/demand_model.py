from datetime import date, timedelta
from typing import Dict, List

import numpy as np
from sqlalchemy.orm import Session

from .. import models


def simple_moving_average_forecast(
    db: Session,
    horizon_days: int = 30,
    window: int = 7,
) -> Dict[str, List[Dict]]:
    """
    Very small, self-contained example "ML" model for demand forecasting.

    For each product:
    - Collect historical daily quantities.
    - Compute a simple moving average over the last `window` days.
    - Project that average as a flat forecast for the next `horizon_days`.

    Returns a dictionary keyed by product name with a list of
    { "date": <date>, "predicted_quantity": <float> } entries.

    In a real deployment, you can:
    - Replace this with ARIMA/Prophet/LSTM models.
    - Train models offline and just load them here.
    """
    # Fetch all demand history joined with products.
    rows = (
        db.query(models.Product.name, models.DemandHistory.date, models.DemandHistory.quantity)
        .join(models.DemandHistory, models.Product.id == models.DemandHistory.product_id)
        .order_by(models.Product.name, models.DemandHistory.date)
        .all()
    )

    series: Dict[str, List[Dict[str, float]]] = {}
    for name, d, q in rows:
        series.setdefault(name, []).append({"date": d, "quantity": q})

    forecasts: Dict[str, List[Dict]] = {}
    today = date.today()

    for product_name, points in series.items():
        if not points:
            continue

        # Use last `window` points (or all if fewer) to compute a moving average.
        quantities = np.array([p["quantity"] for p in points[-window:]])
        avg = float(np.mean(quantities))

        product_forecast: List[Dict] = []
        for i in range(1, horizon_days + 1):
            target_date = today + timedelta(days=i)
            product_forecast.append(
                {
                    "date": target_date,
                    "predicted_quantity": avg,
                }
            )

        forecasts[product_name] = product_forecast

    return forecasts

