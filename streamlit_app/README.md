# AI Forecasting & Planning – Streamlit app

Same features as the React dashboard: **Demand forecasting**, **Workforce planning**, **Budget prediction**, plus **Excel/PDF export**.

## Run locally

From the **project root** (parent of `streamlit_app/`):

```bash
pip install -r streamlit_app/requirements.txt
streamlit run streamlit_app/app.py
```

Then open **http://localhost:8501**.

## Deploy to Streamlit Community Cloud

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Set **Main file path** to `streamlit_app/app.py`.
4. In **Advanced settings**, set **Requirements file** to `streamlit_app/requirements.txt`.
5. Deploy. Your app will be at `https://<your-app>.streamlit.app`.

See the main [DEPLOYMENT.md](../DEPLOYMENT.md) for more options.
