from datetime import date
from typing import List, Optional

from pydantic import BaseModel


# ---------- Shared / core ----------


class Message(BaseModel):
    """Generic message response schema."""

    message: str


# ---------- Demand forecasting schemas ----------


class DemandRecord(BaseModel):
    """Single historical demand entry."""

    product_name: str
    date: date
    quantity: float


class DemandUploadRequest(BaseModel):
    """
    Request body for uploading demand history via JSON.
    (The CSV upload endpoint will parse CSV into this structure.)
    """

    records: List[DemandRecord]


class DemandForecastPoint(BaseModel):
    """Single forecasted point for a product on a specific date."""

    product_name: str
    date: date
    predicted_quantity: float


class DemandForecastResponse(BaseModel):
    """Response payload containing demand forecast series."""

    horizon_days: int
    forecasts: List[DemandForecastPoint]


# ---------- Workforce planning schemas ----------


class WorkforcePlanRequest(BaseModel):
    """
    Minimal request body for workforce planning.
    In a real app this would include skills, shifts, etc.
    """

    department: str
    start_date: date
    end_date: date
    predicted_daily_demand: float
    productivity_per_employee: float = 10.0  # units per employee per day


class WorkforcePlanEntry(BaseModel):
    date: date
    department: str
    required_headcount: int


class WorkforcePlanResponse(BaseModel):
    plans: List[WorkforcePlanEntry]


# ---------- Budget prediction schemas ----------


class BudgetRecord(BaseModel):
    date: date
    revenue: float
    expenses: float
    workforce_cost: float


class BudgetUploadRequest(BaseModel):
    records: List[BudgetRecord]


class BudgetForecastPoint(BaseModel):
    date: date
    projected_revenue: float
    projected_expenses: float
    projected_workforce_cost: float


class BudgetForecastResponse(BaseModel):
    horizon_months: int
    forecasts: List[BudgetForecastPoint]

