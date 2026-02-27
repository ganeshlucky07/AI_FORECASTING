import React, { useState } from "react";
import { apiFetch } from "../api";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from "recharts";

interface ForecastPoint {
  product_name: string;
  date: string;
  predicted_quantity: number;
}

interface ForecastResponse {
  horizon_days: number;
  forecasts: ForecastPoint[];
}

// Demand forecasting page:
// - Upload CSV of historical demand.
// - Call backend /api/demand/forecast to visualize predictions.
export const DemandPage: React.FC = () => {
  const [uploadMessage, setUploadMessage] = useState<string | null>(null);
  const [forecast, setForecast] = useState<ForecastResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const downloadFile = async (url: string, filename: string) => {
    const res = await apiFetch(url);
    const blob = await res.blob();
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(link.href);
  };

  const handleCsvUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setUploadMessage(null);

    const res = await apiFetch("/api/demand/upload_csv", {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    setUploadMessage(data.message ?? "Upload completed.");
  };

  const loadForecast = async () => {
    setLoading(true);
    try {
      const res = await apiFetch("/api/demand/forecast?horizon_days=30");
      const data = (await res.json()) as ForecastResponse;
      setForecast(data);
    } finally {
      setLoading(false);
    }
  };

  // Group forecast points by product to create separate series.
  const groupedByProduct: Record<string, { date: string; [key: string]: number | string }[]> =
    {};

  if (forecast) {
    forecast.forecasts.forEach((p) => {
      const key = p.product_name;
      if (!groupedByProduct[key]) {
        groupedByProduct[key] = [];
      }
      groupedByProduct[key].push({
        date: p.date,
        [key]: p.predicted_quantity
      });
    });
  }

  // Merge all product series into a single array keyed by date for charting.
  const mergedSeries: { date: string; [key: string]: number | string }[] = [];
  if (forecast) {
    const byDate: Record<string, { [key: string]: number | string }> = {};

    forecast.forecasts.forEach((p) => {
      if (!byDate[p.date]) {
        byDate[p.date] = { date: p.date };
      }
      byDate[p.date][p.product_name] = p.predicted_quantity;
    });

    Object.values(byDate)
      .sort((a, b) => String(a.date).localeCompare(String(b.date)))
      .forEach((row) => mergedSeries.push(row));
  }

  const productNames = forecast
    ? Array.from(new Set(forecast.forecasts.map((f) => f.product_name)))
    : [];

  return (
    <section>
      <h2>Demand Forecasting</h2>
      <p>
        Upload historical sales or usage data and generate short-term demand forecasts per product.
      </p>

      <div className="card">
        <h3>1. Upload demand history (CSV)</h3>
        <p className="hint">
          Expected columns: <code>product_name,date,quantity</code> with dates in YYYY-MM-DD.
        </p>
        <input type="file" accept=".csv" onChange={handleCsvUpload} />
        {uploadMessage && <p className="status">{uploadMessage}</p>}
      </div>

      <div className="card">
        <h3>2. Generate forecast</h3>
        <button onClick={loadForecast} disabled={loading}>
          {loading ? "Loading..." : "Run 30-day forecast"}
        </button>
        {forecast && (
          <div style={{ marginTop: "0.75rem", display: "flex", gap: "0.5rem", flexWrap: "wrap" }}>
            <button onClick={() => downloadFile("/api/demand/export/excel?horizon_days=30", "demand_forecast.xlsx")}>
              Download Excel
            </button>
            <button onClick={() => downloadFile("/api/demand/export/pdf?horizon_days=30", "demand_forecast.pdf")}>
              Download PDF
            </button>
          </div>
        )}
      </div>

      {forecast && (
        <div className="card">
          <h3>Forecast results</h3>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={350}>
              <LineChart data={mergedSeries}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                {productNames.map((name, idx) => (
                  <Line
                    key={name}
                    type="monotone"
                    dataKey={name}
                    stroke={["#2563eb", "#16a34a", "#f97316", "#dc2626"][idx % 4]}
                    dot={false}
                  />
                ))}
              </LineChart>
            </ResponsiveContainer>
          </div>
          <p className="hint">
            Each line represents predicted daily demand for a product. You can extend this view to
            show confidence intervals or multiple scenarios.
          </p>
        </div>
      )}
    </section>
  );
};

