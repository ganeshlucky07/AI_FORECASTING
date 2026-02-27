# Deploy to Vercel (Frontend Only)

This guide explains how to deploy the React frontend to **Vercel's free tier** and connect it to a backend deployed elsewhere (e.g., Render).

## Architecture

- **Frontend (Vercel)**: React + Vite app
- **Backend (Render)**: FastAPI + SQLite (free tier)

---

## Step 1: Deploy Backend to Render (Free Tier)

The FastAPI backend cannot run on Vercel (serverless functions only). Deploy it to Render first.

1. **Push code to GitHub** (if not already done)

2. **Go to [render.com](https://render.com)** and sign up/log in

3. **Create New Web Service**:
   - Click **New** → **Web Service**
   - Connect your GitHub repo
   - Select `AI_FORECASTING` repository

4. **Configure Service**:
   - **Name**: `ai-forecasting-api`
   - **Runtime**: Docker
   - **Dockerfile Path**: `./Dockerfile`
   - **Docker Context**: `.`
   - **Branch**: `main`

5. **Set Environment Variables**:
   ```
   SERVE_FRONTEND=0
   CORS_ORIGINS=*
   ```

6. **Create Web Service**

7. **Wait for deployment** and note the URL (e.g., `https://ai-forecasting-api.onrender.com`)

---

## Step 2: Deploy Frontend to Vercel

### Option A: Via Vercel Dashboard (Recommended)

1. **Go to [vercel.com](https://vercel.com)** and sign up/log in with GitHub

2. **Add New Project**:
   - Click **Add New...** → **Project**
   - Import your GitHub repository

3. **Configure Project**:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

4. **Set Environment Variables**:
   ```
   VITE_API_URL=https://your-backend.onrender.com
   ```
   (Replace with your actual Render backend URL, no trailing slash)

5. **Deploy**

6. **Your app will be live** at `https://your-project.vercel.app`

### Option B: Via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend folder
cd frontend

# Link and deploy
vercel

# Set environment variable
vercel env add VITE_API_URL
# Enter: https://your-backend.onrender.com

# Redeploy
vercel --prod
```

---

## Step 3: Update Backend CORS (After Frontend Deploy)

Once your Vercel frontend is live, restrict CORS for security:

1. Go to your Render dashboard
2. Open your backend service
3. Update environment variables:
   ```
   CORS_ORIGINS=https://your-frontend.vercel.app
   ```
4. The service will redeploy automatically

---

## Environment Variables Summary

| Variable | Location | Value |
|----------|----------|-------|
| `VITE_API_URL` | Vercel | `https://your-backend.onrender.com` |
| `CORS_ORIGINS` | Render | `https://your-frontend.vercel.app` or `*` |
| `SERVE_FRONTEND` | Render | `0` (backend only) |

---

## Local Development

For local development, the Vite proxy in `vite.config.ts` handles API calls:

```bash
cd frontend
npm install
npm run dev
```

The frontend will call `http://localhost:8000` via the proxy (no env var needed locally).

---

## Troubleshooting

### CORS Errors
- Ensure `CORS_ORIGINS` on Render includes your Vercel domain
- Check that you're not using a trailing slash on `VITE_API_URL`

### API Not Responding
- Verify your Render backend is running (check the dashboard)
- Confirm `VITE_API_URL` is set correctly in Vercel

### Build Failures
- Ensure `vercel.json` is in the `frontend/` folder
- Check that `dist` folder is created during build
