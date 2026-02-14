import React, { useState } from "react";

interface BudgetForecastPoint {
  date: string;
  projected_revenue: number;
  projected_expenses: number;
  projected_workforce_cost: number;
}

interface BudgetForecastResponse {
  horizon_months: number;
  forecasts: BudgetForecastPoint[];
}

// Budget prediction page:
// - Upload historical budget data.
// - Call backend /api/budget/forecast to see projected values.
export const BudgetPage: React.FC = () => {
  const [uploadMessage, setUploadMessage] = useState<string | null>(null);
  const [forecast, setForecast] = useState<BudgetForecastResponse | null>(null);

  const downloadExcel = async () => {
    const res = await fetch("/api/budget/export/excel?horizon_months=6");
    const blob = await res.blob();
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "budget_forecast.xlsx";
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(link.href);
  };

  const handleJsonUpload = async (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    try {
      const parsed = JSON.parse(e.target.value);
      const res = await fetch("/api/budget/upload_history", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(parsed)
      });
      const data = await res.json();
      setUploadMessage(data.message ?? "Upload completed.");
    } catch (err) {
      setUploadMessage("Invalid JSON format.");
    }
  };

  const loadForecast = async () => {
    const res = await fetch("/api/budget/forecast?horizon_months=6");
    const data = (await res.json()) as BudgetForecastResponse;
    setForecast(data);
  };

  return (
    <section>
      <h2>Budget Prediction</h2>
      <p>
        Use historical revenues, expenses, and workforce costs to project budget requirements and
        spot potential overspending.
      </p>

      <div className="card">
        <h3>1. Upload budget history (JSON)</h3>
        <p className="hint">
          Provide an object of the form{" "}
          <code>
            &#123; "records": [ &#123; "date": "2024-01-01", "revenue": 1000, "expenses": 800,
            "workforce_cost": 300 &#125;, ... ] &#125;
          </code>
          . You can easily export this from your own systems.
        </p>
        <textarea
          rows={6}
          className="json-input"
          placeholder='{"records":[{"date":"2024-01-01","revenue":1000,"expenses":800,"workforce_cost":300}]}'
          onBlur={handleJsonUpload}
        />
        {uploadMessage && <p className="status">{uploadMessage}</p>}
      </div>

      <div className="card">
        <h3>2. Generate 6‑month forecast</h3>
        <button onClick={loadForecast}>Run forecast</button>
        {forecast && (
          <button style={{ marginLeft: "0.5rem" }} onClick={downloadExcel}>
            Download Excel
          </button>
        )}
      </div>

      {forecast && (
        <div className="card">
          <h3>Projected budget</h3>
          <table className="table">
            <thead>
              <tr>
                <th>Month</th>
                <th>Projected revenue</th>
                <th>Projected expenses</th>
                <th>Projected workforce cost</th>
              </tr>
            </thead>
            <tbody>
              {forecast.forecasts.map((f) => (
                <tr key={f.date}>
                  <td>{f.date}</td>
                  <td>{f.projected_revenue.toFixed(2)}</td>
                  <td>{f.projected_expenses.toFixed(2)}</td>
                  <td>{f.projected_workforce_cost.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <p className="hint">
            Extend this module with scenario analysis (e.g., demand spikes or workforce changes) and
            more advanced time‑series models.
          </p>
        </div>
      )}
    </section>
  );
};

