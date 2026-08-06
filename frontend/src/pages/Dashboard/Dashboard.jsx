// Dashboard.jsx
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import useAuth from "../../hooks/useAuth";
import {
  getDashboardSummary,
  getRecentPredictions,
} from "../../services/dashboardService";
import Loader from "../../components/Loader/Loader";
import "./Dashboard.css";

function Dashboard() {
  const { user } = useAuth();
  const [summary, setSummary] = useState(null);
  const [recent, setRecent] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let mounted = true;

    async function loadDashboard() {
      try {
        const [summaryData, predictionData] = await Promise.all([
          getDashboardSummary(),
          getRecentPredictions(),
        ]);

        if (!mounted) return;

        setSummary(summaryData);
        setRecent(predictionData);
      } catch (err) {
        if (!mounted) return;
        setError(
          err.response?.data?.message ||
            "Unable to sync core platform telemetries.",
        );
      } finally {
        if (mounted) setLoading(false);
      }
    }

    loadDashboard();

    return () => {
      mounted = false;
    };
  }, []);

  if (loading) {
    return <Loader text="Synchronizing Diagnostic Metrics..." />;
  }

  return (
    <main className="dashboard-view" aria-label="Medical Analytics Workspace">
      {/* Workspace Header */}
      <header className="dashboard-header-panel">
        <div className="welcome-meta-block">
          <h1>Welcome back, Dr. {user?.name || "Practitioner"}</h1>
          <p>Monitor and track neural framework runtime analysis logs.</p>
        </div>

        <Link to="/prediction" className="dashboard-primary-action-btn">
          <svg
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2.5"
          >
            <line x1="12" y1="5" x2="12" y2="19" />
            <line x1="5" y1="12" x2="19" y2="12" />
          </svg>
          <span>New Pipeline Task</span>
        </Link>
      </header>

      {/* Exception Fallbacks */}
      {error && (
        <div className="dashboard-error-banner" role="alert">
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2.5"
          >
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="8" x2="12" y2="12" />
            <line x1="12" y1="16" x2="12.01" y2="16" />
          </svg>
          <span>{error}</span>
        </div>
      )}

      {/* Analytics Counter Grid Array */}
      {summary && (
        <section
          className="analytics-summary-grid"
          aria-label="Performance Aggregations"
        >
          <div className="analytics-summary-card">
            <span className="summary-card-label">
              Cumulative Processing Tasks
            </span>
            <h2 className="summary-card-metric">{summary.total_predictions}</h2>
          </div>

          <div className="analytics-summary-card">
            <span className="summary-card-label">
              Validation Target Precision
            </span>
            <h2 className="summary-card-metric">90.5%</h2>
          </div>

          <div className="analytics-summary-card">
            <span className="summary-card-label">Mean Confidence Interval</span>
            <h2 className="summary-card-metric">
              {summary.average_confidence}%
            </h2>
          </div>

          <div className="analytics-summary-card">
            <span className="summary-card-label">Active Inference Hubs</span>
            <h2 className="summary-card-metric">{summary.models}</h2>
          </div>
        </section>
      )}

      {/* Historic Logs Data Workspace */}
      <section
        className="dashboard-records-block"
        aria-labelledby="records-table-heading"
      >
        <div className="records-block-header">
          <h2 id="records-table-heading">Recent Detection Stream</h2>
          <Link to="/history" className="records-view-all-link">
            <span>Audit Trail</span>
            <svg
              width="14"
              height="14"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2.5"
            >
              <line x1="5" y1="12" x2="19" y2="12" />
              <polyline points="12 5 19 12 12 19" />
            </svg>
          </Link>
        </div>

        {recent.length === 0 ? (
          <div className="records-empty-state">
            <svg
              width="32"
              height="32"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
              <polyline points="14 2 14 8 20 8" />
            </svg>
            <p>
              No operational diagnostic records found in recent ingestion
              vectors.
            </p>
          </div>
        ) : (
          <div className="table-viewport-wrapper">
            <table className="records-data-table">
              <thead>
                <tr>
                  <th>Ingestion Timestamp</th>
                  <th>Classification Class</th>
                  <th>Confidence Index</th>
                  <th>Execution Pipeline</th>
                </tr>
              </thead>
              <tbody>
                {recent.map((item) => (
                  <tr key={item.id}>
                    <td className="timestamp-cell">
                      {item.created_at
                        ? new Date(item.created_at).toLocaleString()
                        : "—"}
                    </td>
                    <td>
                      <span
                        className={`status-badge-token ${item.prediction?.toLowerCase().includes("pneumonia") ? "is-positive" : "is-negative"}`}
                      >
                        {item.prediction}
                      </span>
                    </td>
                    <td className="metric-cell-token">{item.confidence}%</td>
                    <td className="pipeline-cell-token">{item.model}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </main>
  );
}

export default Dashboard;
