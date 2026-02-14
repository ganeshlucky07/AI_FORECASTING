# Deploy AI Forecasting & Planning Agent

This project can be deployed as a **Streamlit app**, a **single Docker app** (React + FastAPI), or **separate frontend and backend** services.

---

## Deploy with Streamlit (Streamlit Community Cloud)

The repo includes a **Streamlit dashboard** in `streamlit_app/` with the same features: demand forecast, workforce planning, budget prediction, and Excel/PDF export. No backend server needed.

### Run locally

From the **project root**:

```bash
pip install -r streamlit_app/requirements.txt
streamlit run streamlit_app/app.py
```

Open the URL shown (usually `http://localhost:8501`).

### Deploy to Streamlit Community Cloud (free)

1. **Push the project to GitHub** (same repo as above).

2. Go to **[share.streamlit.io](https://share.streamlit.io)** and sign in with GitHub.

3. Click **New app**, then:
   - **Repository**: your repo (e.g. `your-username/AI_FORECASTING`).
   - **Branch**: `main` (or your default).
   - **Main file path**: `streamlit_app/app.py`
   - **App URL**: choose a subdomain (e.g. `ai-forecasting` → `https://ai-forecasting.streamlit.app`).

4. Click **Deploy**. Streamlit Cloud will use `streamlit_app/requirements.txt` (set **Advanced settings** → **Requirements file** to `streamlit_app/requirements.txt` if it doesn’t auto-detect).

5. When the build finishes, open your app URL. Upload CSVs in each tab to try demand and budget; use the form for workforce planning and use the download buttons to export Excel/PDF.

---

## Option 1: Deploy to Render.com (Docker – React + FastAPI)

1. **Push your code to GitHub**  
   Create a repo and push this project (no need to push `node_modules`, `.venv`, or `*.db`—add them to `.gitignore` if needed).

2. **Sign up / log in at [Render](https://render.com)**.

3. **New Web Service**  
   - Dashboard → **New** → **Web Service**.  
   - Connect your GitHub repo and select the `AI_FORECASTING` repo (or the one containing this project).

4. **Configure the service**  
   - **Runtime**: Docker.  
   - **Dockerfile path**: `./Dockerfile` (project root).  
   - **Name**: e.g. `ai-forecasting`.  
   - **Region**: choose the closest to you.

5. **Environment variables (optional)**  
   - `SERVE_FRONTEND` = `1`  
   - `STATIC_DIR` = `/app/static`  
   (These are already set in `render.yaml` if you use the blueprint.)

6. **Deploy**  
   Click **Create Web Service**. Render will build the Docker image and run it. When the build finishes, open the URL (e.g. `https://ai-forecasting.onrender.com`).

7. **Optional: use the blueprint**  
   If your repo has `render.yaml` in the root, you can use **Blueprint** when creating the service so Render reads the Dockerfile and env from the file.

---

## Option 2: Deploy with Docker locally or on any VPS

From the **project root** (where `Dockerfile` and `requirements.txt` are):

```bash
docker build -t ai-forecasting .
docker run -p 8000:8000 -e SERVE_FRONTEND=1 -e STATIC_DIR=/app/static ai-forecasting
```

Then open **http://localhost:8000** (or your server’s host and port). The same image can be run on a VPS (e.g. DigitalOcean, AWS EC2) and exposed via Nginx or a reverse proxy.

---

## Option 3: Split frontend and backend (e.g. Vercel + Render)

- **Backend (Render)**  
  - Deploy only the backend: use `backend/Dockerfile` and set the service root/context so it builds the backend.  
  - Set **CORS**: add env `CORS_ORIGINS` = `https://your-frontend.vercel.app`.

- **Frontend (Vercel)**  
  - In the repo, set the **root directory** to `frontend`.  
  - Add env **VITE_API_URL** = `https://your-backend.onrender.com` (no trailing slash).  
  - In the frontend, call the API with `import.meta.env.VITE_API_URL + '/api/...'` or configure Vite to use that base for `/api` in production.

---

## Environment variables reference

| Variable           | Description                                      | Default / note                    |
|--------------------|--------------------------------------------------|-----------------------------------|
| `DATABASE_URL`     | PostgreSQL or SQLite URL                         | `sqlite:///./forecasting.db`      |
| `CORS_ORIGINS`     | Comma-separated allowed origins                  | `*` (restrict in production)      |
| `SERVE_FRONTEND`   | Set to `1` to serve built frontend from FastAPI | Unset in backend-only deploy      |
| `STATIC_DIR`       | Path to built frontend (e.g. `/app/static`)     | Set in Docker / Render            |

---

## After deployment

- Use **https://your-app.onrender.com** (or your URL) to open the dashboard.  
- Data is stored in SQLite inside the container by default; it will be lost on redeploy unless you add a **persistent disk** (Render) or switch to an external **PostgreSQL** and set `DATABASE_URL`.
