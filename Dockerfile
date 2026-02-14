# Production Dockerfile: builds frontend and serves it from FastAPI (single deploy).
# Use from project root: docker build -t ai-forecasting .

# ---- Frontend build ----
FROM node:20-alpine AS frontend
WORKDIR /app
COPY frontend/package.json ./
COPY frontend/ ./
RUN npm install
RUN npm run build

# ---- Backend + static serve ----
FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY --from=frontend /app/dist ./static

# Same host: frontend calls /api on same origin; no CORS change needed.
ENV PYTHONPATH=/app
ENV SERVE_FRONTEND=1
ENV STATIC_DIR=/app/static
ENV PORT=8000

EXPOSE 8000
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
