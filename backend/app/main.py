import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .routers import demand, workforce, budget
from .database import engine
from . import models


def create_app() -> FastAPI:
    """
    Application factory for the AI Forecasting & Planning backend.

    This wires together:
    - CORS
    - Routers for each module (demand, workforce, budget)
    - Optional static frontend (when SERVE_FRONTEND=1 and static dir present)
    """
    app = FastAPI(
        title="AI Forecasting & Planning Agent",
        version="0.1.0",
        description="Backend API for demand forecasting, workforce planning, and budget prediction.",
    )

    # CORS: use CORS_ORIGINS env in production (e.g. "https://yourapp.com"); "*" for dev.
    cors_origins = os.getenv("CORS_ORIGINS", "").strip()
    origins = [o.strip() for o in cors_origins.split(",") if o.strip()] if cors_origins else ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Create database tables on startup (simple demo approach).
    # In a production system, you'd use proper migrations instead.
    models.Base.metadata.create_all(bind=engine)

    # Register modular routers (must be before static mount so /api takes precedence).
    app.include_router(demand.router, prefix="/api/demand", tags=["Demand"])
    app.include_router(workforce.router, prefix="/api/workforce", tags=["Workforce"])
    app.include_router(budget.router, prefix="/api/budget", tags=["Budget"])

    # Production: serve frontend static files from same host (single deploy).
    static_dir = os.getenv("STATIC_DIR", "").strip()
    if os.getenv("SERVE_FRONTEND", "").strip() == "1" and static_dir and os.path.isdir(static_dir):
        app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

    return app


app = create_app()

