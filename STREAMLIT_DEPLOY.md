# Deploy this project on Streamlit Community Cloud

Your repo: **https://github.com/ganeshlucky07/AI_FORECASTING**

## Steps (do this once)

1. **Open:** [share.streamlit.io](https://share.streamlit.io) and sign in with **GitHub** (use the same account: ganeshlucky07).

2. **New app**
   - Click **"New app"**.

3. **Configure the app**
   - **Repository:** `ganeshlucky07/AI_FORECASTING`
   - **Branch:** `main`
   - **Main file path:** `streamlit_app/app.py`

4. **Advanced settings** (click to expand)
   - **Requirements file:** `streamlit_app/requirements.txt`  
     (Streamlit Cloud will install from this file.)
   - **Python version:** 3.11 (or leave default).

5. **App URL**
   - Choose a subdomain, e.g. `ai-forecasting` → your app will be:  
     **https://ai-forecasting.streamlit.app**

6. **Deploy**
   - Click **"Deploy!"**.  
   - Wait a few minutes for the build. When it’s done, open the app URL.

## After deployment

- Use the three tabs: **Demand Forecast**, **Workforce Planning**, **Budget Prediction**.
- Upload CSVs (demand: `product_name`, `date`, `quantity`; budget: `date`, `revenue`, `expenses`, `workforce_cost`).
- Use the download buttons to export **Excel** and **PDF**.

If the build fails, check the logs on the app page; usually it’s a missing dependency in `streamlit_app/requirements.txt`.
