import React, { useState } from "react";

interface WorkforcePlanEntry {
  date: string;
  department: string;
  required_headcount: number;
}

interface WorkforcePlanResponse {
  plans: WorkforcePlanEntry[];
}

// Workforce planning page:
// - Accepts simple inputs for department, period, and demand.
// - Calls backend /api/workforce/plan to generate staffing suggestions.
export const WorkforcePage: React.FC = () => {
  const [department, setDepartment] = useState("Operations");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [demand, setDemand] = useState(100);
  const [productivity, setProductivity] = useState(10);
  const [plan, setPlan] = useState<WorkforcePlanResponse | null>(null);

  const downloadExcel = async () => {
    const res = await fetch("/api/workforce/export/excel");
    const blob = await res.blob();
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "workforce_plans.xlsx";
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(link.href);
  };

  const submitPlan = async () => {
    if (!startDate || !endDate) return;

    const body = {
      department,
      start_date: startDate,
      end_date: endDate,
      predicted_daily_demand: demand,
      productivity_per_employee: productivity
    };

    const res = await fetch("/api/workforce/plan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });
    const data = (await res.json()) as WorkforcePlanResponse;
    setPlan(data);
  };

  return (
    <section>
      <h2>Workforce Planning</h2>
      <p>
        Optimize staffing levels based on demand and productivity assumptions. This demo uses a
        simple rule-based model you can later upgrade to an optimization solver.
      </p>

      <div className="card grid-2">
        <div>
          <label>
            Department
            <input value={department} onChange={(e) => setDepartment(e.target.value)} />
          </label>
          <label>
            Start date
            <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
          </label>
          <label>
            End date
            <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
          </label>
        </div>
        <div>
          <label>
            Predicted daily demand
            <input
              type="number"
              value={demand}
              onChange={(e) => setDemand(Number(e.target.value))}
            />
          </label>
          <label>
            Units per employee per day
            <input
              type="number"
              value={productivity}
              onChange={(e) => setProductivity(Number(e.target.value))}
            />
          </label>

          <button onClick={submitPlan}>Generate workforce plan</button>
          {plan && (
            <button style={{ marginLeft: "0.5rem" }} onClick={downloadExcel}>
              Download Excel
            </button>
          )}
        </div>
      </div>

      {plan && (
        <div className="card">
          <h3>Suggested staffing levels</h3>
          <table className="table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Department</th>
                <th>Required headcount</th>
              </tr>
            </thead>
            <tbody>
              {plan.plans.map((p) => (
                <tr key={p.date}>
                  <td>{p.date}</td>
                  <td>{p.department}</td>
                  <td>{p.required_headcount}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <p className="hint">
            Extend this by incorporating individual employee skills, shifts, and labor rules, then
            solving with linear programming or constraint programming.
          </p>
        </div>
      )}
    </section>
  );
};

