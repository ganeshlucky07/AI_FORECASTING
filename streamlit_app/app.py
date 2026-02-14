"""
AI Forecasting & Planning Agent – Streamlit dashboard.
Run from repo root: streamlit run streamlit_app/app.py
Deploy: push to GitHub and deploy on share.streamlit.io
"""
import os
import sys
# Allow imports from streamlit_app when run from repo root (e.g. Streamlit Cloud).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
from datetime import date, timedelta

from lib.demand import forecast_demand
from lib.workforce import plan_workforce
from lib.budget import forecast_budget
from lib.export import rows_to_excel, simple_table_pdf

st.set_page_config(
    page_title="AI Forecasting & Planning",
    page_icon="📊",
    layout="wide",
)

st.title("📊 AI Forecasting & Planning Agent")
st.caption("Demand forecasting, workforce planning, and budget prediction.")

tab1, tab2, tab3 = st.tabs(["Demand Forecast", "Workforce Planning", "Budget Prediction"])

# ----- Demand -----
with tab1:
    st.subheader("Demand Forecasting")
    st.markdown("Upload historical sales/usage CSV (columns: `product_name`, `date`, `quantity`). Then run a 30-day forecast.")
    demand_file = st.file_uploader("Upload demand CSV", type=["csv"], key="demand_csv")
    demand_df = None
    if demand_file:
        demand_df = pd.read_csv(demand_file)
        st.dataframe(demand_df.head(10), use_container_width=True)
    horizon = st.slider("Forecast horizon (days)", 7, 90, 30, key="demand_horizon")
    if st.button("Run demand forecast", key="run_demand"):
        if demand_df is not None and not demand_df.empty:
            forecasts = forecast_demand(demand_df, horizon_days=horizon)
            st.session_state["demand_forecasts"] = forecasts
        else:
            st.warning("Upload a CSV first.")

    if "demand_forecasts" in st.session_state and st.session_state["demand_forecasts"]:
        forecasts = st.session_state["demand_forecasts"]
        df_f = pd.DataFrame(forecasts)
        st.subheader("Forecast results")
        st.line_chart(
            df_f.pivot_table(index="date", columns="product_name", values="predicted_quantity").fillna(0)
        )
        st.dataframe(df_f, use_container_width=True)
        col1, col2 = st.columns(2)
        with col1:
            excel_buf = rows_to_excel(forecasts, ["product_name", "date", "predicted_quantity"])
            st.download_button("Download Excel", data=excel_buf, file_name="demand_forecast.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        with col2:
            pdf_rows = [(r["product_name"], str(r["date"]), r["predicted_quantity"]) for r in forecasts[:200]]
            pdf_buf = simple_table_pdf("Demand Forecast", ["product", "date", "predicted_qty"], pdf_rows)
            st.download_button("Download PDF", data=pdf_buf, file_name="demand_forecast.pdf", mime="application/pdf")

# ----- Workforce -----
with tab2:
    st.subheader("Workforce Planning")
    st.markdown("Set department, date range, and demand to get suggested headcount per day.")
    c1, c2 = st.columns(2)
    with c1:
        dept = st.text_input("Department", value="Operations", key="wf_dept")
        start_d = st.date_input("Start date", value=date.today(), key="wf_start")
        end_d = st.date_input("End date", value=date.today() + timedelta(days=13), key="wf_end")
    with c2:
        daily_demand = st.number_input("Predicted daily demand", min_value=1, value=100, key="wf_demand")
        productivity = st.number_input("Units per employee per day", min_value=1, value=10, key="wf_prod")
    if st.button("Generate workforce plan", key="run_wf"):
        if end_d >= start_d:
            plans = plan_workforce(dept, start_d, end_d, daily_demand, productivity)
            st.session_state["workforce_plans"] = plans
        else:
            st.warning("End date must be after start date.")

    if "workforce_plans" in st.session_state and st.session_state["workforce_plans"]:
        plans = st.session_state["workforce_plans"]
        df_w = pd.DataFrame(plans)
        st.dataframe(df_w, use_container_width=True)
        excel_w = rows_to_excel(plans, ["date", "department", "required_headcount"])
        st.download_button("Download Excel", data=excel_w, file_name="workforce_plans.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key="dl_wf")

# ----- Budget -----
with tab3:
    st.subheader("Budget Prediction")
    st.markdown("Upload budget history CSV with columns: `date`, `revenue`, `expenses`, `workforce_cost`. Then run a 6‑month projection.")
    budget_file = st.file_uploader("Upload budget CSV", type=["csv"], key="budget_csv")
    budget_df = None
    if budget_file:
        budget_df = pd.read_csv(budget_file)
        st.dataframe(budget_df.head(10), use_container_width=True)
    budget_months = st.slider("Forecast horizon (months)", 1, 24, 6, key="budget_months")
    if st.button("Run budget forecast", key="run_budget"):
        if budget_df is not None and not budget_df.empty:
            budget_forecasts = forecast_budget(budget_df, horizon_months=budget_months)
            st.session_state["budget_forecasts"] = budget_forecasts
        else:
            st.warning("Upload a budget CSV first.")

    if "budget_forecasts" in st.session_state and st.session_state["budget_forecasts"]:
        bf = st.session_state["budget_forecasts"]
        df_b = pd.DataFrame(bf)
        st.dataframe(df_b, use_container_width=True)
        excel_b = rows_to_excel(
            bf,
            ["date", "projected_revenue", "projected_expenses", "projected_workforce_cost"],
        )
        st.download_button("Download Excel", data=excel_b, file_name="budget_forecast.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key="dl_budget")
