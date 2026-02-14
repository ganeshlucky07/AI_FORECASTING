import React, { useState } from "react";
import { DemandPage } from "./components/DemandPage";
import { WorkforcePage } from "./components/WorkforcePage";
import { BudgetPage } from "./components/BudgetPage";

type TabKey = "demand" | "workforce" | "budget";

// Simple layout with three tabs for the three modules.
export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<TabKey>("demand");

  return (
    <div className="app-root">
      <header className="app-header">
        <h1>AI Forecasting &amp; Planning Agent</h1>
        <p className="subtitle">
          Demand forecasting, workforce planning, and budget prediction in one dashboard.
        </p>
      </header>

      <nav className="tab-bar">
        <button
          className={activeTab === "demand" ? "tab active" : "tab"}
          onClick={() => setActiveTab("demand")}
        >
          Demand Forecast
        </button>
        <button
          className={activeTab === "workforce" ? "tab active" : "tab"}
          onClick={() => setActiveTab("workforce")}
        >
          Workforce Planning
        </button>
        <button
          className={activeTab === "budget" ? "tab active" : "tab"}
          onClick={() => setActiveTab("budget")}
        >
          Budget Prediction
        </button>
      </nav>

      <main className="app-main">
        {activeTab === "demand" && <DemandPage />}
        {activeTab === "workforce" && <WorkforcePage />}
        {activeTab === "budget" && <BudgetPage />}
      </main>
    </div>
  );
};

