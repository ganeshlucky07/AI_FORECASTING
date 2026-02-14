from typing import List

from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..ml.demand_model import simple_moving_average_forecast
from ..utils import exporters

import csv
import io
from datetime import datetime

router = APIRouter()


@router.post("/upload_csv", response_model=schemas.Message)
async def upload_demand_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Upload historical demand data as CSV.

    Expected columns:
    - product_name
    - date (YYYY-MM-DD)
    - quantity
    """
    content = await file.read()
    text_stream = io.StringIO(content.decode("utf-8"))
    reader = csv.DictReader(text_stream)

    for row in reader:
        product_name = row["product_name"].strip()
        date_str = row["date"].strip()
        quantity = float(row["quantity"])

        # Get or create product.
        product = (
            db.query(models.Product)
            .filter(models.Product.name == product_name)
            .first()
        )
        if product is None:
            product = models.Product(name=product_name)
            db.add(product)
            db.flush()  # assign id

        d = datetime.strptime(date_str, "%Y-%m-%d").date()
        record = models.DemandHistory(
            product_id=product.id,
            date=d,
            quantity=quantity,
        )
        db.add(record)

    db.commit()
    return schemas.Message(message="Demand CSV uploaded successfully.")


@router.post("/upload_json", response_model=schemas.Message)
def upload_demand_json(
    payload: schemas.DemandUploadRequest,
    db: Session = Depends(get_db),
):
    """
    Alternative JSON-based upload for demand history.
    """
    for rec in payload.records:
        product = (
            db.query(models.Product)
            .filter(models.Product.name == rec.product_name)
            .first()
        )
        if product is None:
            product = models.Product(name=rec.product_name)
            db.add(product)
            db.flush()

        record = models.DemandHistory(
            product_id=product.id,
            date=rec.date,
            quantity=rec.quantity,
        )
        db.add(record)

    db.commit()
    return schemas.Message(message="Demand JSON uploaded successfully.")


@router.get("/forecast", response_model=schemas.DemandForecastResponse)
def forecast_demand(
    horizon_days: int = 30,
    db: Session = Depends(get_db),
):
    """
    Run a simple moving-average based demand forecast for all products.

    The frontend can visualize this as line charts.
    """
    raw = simple_moving_average_forecast(db=db, horizon_days=horizon_days)

    forecasts: List[schemas.DemandForecastPoint] = []
    for product_name, series in raw.items():
        for point in series:
            forecasts.append(
                schemas.DemandForecastPoint(
                    product_name=product_name,
                    date=point["date"],
                    predicted_quantity=point["predicted_quantity"],
                )
            )

    return schemas.DemandForecastResponse(
        horizon_days=horizon_days,
        forecasts=forecasts,
    )


@router.get("/export/excel")
def export_demand_forecast_excel(
    horizon_days: int = 30,
    db: Session = Depends(get_db),
):
    """
    Export the demand forecast to an Excel file.

    The forecast is recomputed with the current data to keep the export
    stateless and simple.
    """
    raw = simple_moving_average_forecast(db=db, horizon_days=horizon_days)

    rows = []
    for product_name, series in raw.items():
        for point in series:
            rows.append(
                {
                    "product_name": product_name,
                    "date": point["date"],
                    "predicted_quantity": point["predicted_quantity"],
                }
            )

    columns = ["product_name", "date", "predicted_quantity"]
    output = exporters.rows_to_excel(rows, columns)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": 'attachment; filename="demand_forecast.xlsx"'},
    )


@router.get("/export/pdf")
def export_demand_forecast_pdf(
    horizon_days: int = 30,
    db: Session = Depends(get_db),
):
    """
    Export the demand forecast to a simple tabular PDF.
    """
    raw = simple_moving_average_forecast(db=db, horizon_days=horizon_days)

    headers = ["product", "date", "predicted_qty"]
    table_rows = []
    for product_name, series in raw.items():
        for point in series:
            table_rows.append(
                [
                    product_name,
                    point["date"].isoformat(),
                    point["predicted_quantity"],
                ]
            )

    pdf_buffer = exporters.simple_table_pdf(
        title="Demand Forecast",
        headers=headers,
        rows=table_rows,
    )

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="demand_forecast.pdf"'},
    )

