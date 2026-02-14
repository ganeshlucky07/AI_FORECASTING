## AI Forecasting & Planning Agent – Code Structure & Usage

**Repository:** [github.com/ganeshlucky07/AI_FORECASTING](https://github.com/ganeshlucky07/AI_FORECASTING)

This project is a minimal full‑stack example for an **AI Forecasting & Planning Agent** with three main modules:

- **Demand Forecasting**
- **Workforce Planning**
- **Budget Prediction**

The focus is on a **clean, modular architecture** that you can extend with richer models and business logic.

---

### Backend (FastAPI + SQLite)

- `backend/app/main.py` – FastAPI application factory, CORS, and router registration.
- `backend/app/database.py` – SQLAlchemy engine and `get_db` dependency.
- `backend/app/models.py` – Database models (products, demand history, employees, workforce plans, budget history).
- `backend/app/schemas.py` – Pydantic schemas for request/response bodies.
- `backend/app/ml/demand_model.py` – Example demand model (simple moving average).
- `backend/app/routers/demand.py` – Demand forecasting endpoints:
  - `POST /api/demand/upload_csv` – Upload historical demand as CSV.
  - `POST /api/demand/upload_json` – Upload demand history as JSON.
  - `GET  /api/demand/forecast` – Run a 30‑day moving‑average forecast.
- `backend/app/routers/workforce.py` – Workforce planning endpoint:
  - `POST /api/workforce/plan` – Generate required headcount per day.
- `backend/app/routers/budget.py` – Budget prediction endpoints:
  - `POST /api/budget/upload_history` – Upload historical budget data.
  - `GET  /api/budget/forecast` – Simple 6‑month projection.

The demand module is implemented in a way that you can easily swap the simple moving average logic with **ARIMA/Prophet/LSTM** models.

---

### Frontend (React + Vite)

Located under `frontend/`:

- `package.json`, `vite.config.ts`, `tsconfig.json`
- `index.html` – Root HTML.
- `src/main.tsx` – React entry point.
- `src/App.tsx` – Layout with tabs for the three modules.
- `src/components/DemandPage.tsx` – CSV upload + Recharts line chart for demand forecast.
- `src/components/WorkforcePage.tsx` – Form for workforce plan generation + table results.
- `src/components/BudgetPage.tsx` – JSON upload for budget history + table of forecasts.
- `src/styles.css` – Simple dark dashboard styling.

The frontend calls the backend via `/api/...` paths, which are proxied to `http://localhost:8000` during development by Vite.

---

### Running Locally (without Docker)

1. **Backend**

   ```bash
   cd AI_FORECASTING
   python -m venv .venv
   .venv\Scripts\activate   # On Windows PowerShell: .venv\Scripts\Activate.ps1

   pip install -r requirements.txt
   uvicorn backend.app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`.

   You can inspect interactive docs at:

   - `http://localhost:8000/docs`

2. **Frontend**

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

   Open the printed `http://localhost:5173` URL in your browser.

---

### Running with Docker (backend only example)

From the project root:

```bash
docker compose up --build
```

This starts the FastAPI backend on `http://localhost:8000`. You can still run the frontend locally with `npm run dev` (it will call the same backend URL).

You can extend the compose file with a separate frontend container if needed.

---

### Deploying to production

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for step-by-step instructions. You can deploy as a single Docker app to **Render.com** (free tier), run the image on any VPS, or split frontend (e.g. Vercel) and backend (e.g. Render).

Quick Docker build from project root:

```bash
docker build -t ai-forecasting .
docker run -p 8000:8000 -e SERVE_FRONTEND=1 -e STATIC_DIR=/app/static ai-forecasting
```

Then open `http://localhost:8000` for the full dashboard.

---

### Extending the ML / Optimization Logic

- **Demand Forecasting**
  - Replace `simple_moving_average_forecast` with ARIMA/Prophet/LSTM models.
  - Store trained models per product and load them inside the router.
- **Workforce Planning**
  - Replace the simple rule with a linear programming formulation (e.g. using PuLP or OR‑Tools).
  - Add employee calendars, skills, and constraints to `models.py` and `schemas.py`.
- **Budget Prediction**
  - Use time‑series models or regression with demand/workforce as features.
  - Add scenario inputs (e.g. demand spikes, cost changes) and compute “what if” projections.

The current code is intentionally kept lightweight and well‑commented so you can plug in more advanced AI/ML components over time.

