import { Link } from "react-router-dom";
import Loader from "../../components/Loader/Loader";
import useHistory from "../../hooks/useHistory";
import "./History.css";

function History() {
  const {
    history,
    page,
    setPage,
    search,
    setSearch,
    prediction,
    setPrediction,
    totalPages,
    loading,
    error,
    removePrediction,
  } = useHistory();

  const handleDelete = async (id) => {
    const ok = window.confirm(
      "Are you sure you want to delete this prediction?",
    );

    if (!ok) return;

    await removePrediction(id);
  };

  return (
    <main className="history-page">
      <header className="history-header">
        <div>
          <h1>Prediction History</h1>
          <p className="history-subtitle">
            Review previous AI predictions and patient records.
          </p>
        </div>

        <div className="history-filters">
          <input
            type="text"
            placeholder="Search patient, model, prediction..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />

          <select
            value={prediction}
            onChange={(e) => setPrediction(e.target.value)}
          >
            <option value="">All Results</option>
            <option value="NORMAL">Normal</option>
            <option value="PNEUMONIA">Pneumonia</option>
          </select>
        </div>
      </header>

      {loading && <Loader text="Loading patient history..." />}

      {!loading && error && <div className="error-banner">{error}</div>}

      {!loading && !error && history.length === 0 && (
        <div className="empty-state">No prediction history found.</div>
      )}

      {!loading && !error && history.length > 0 && (
        <div className="table-container">
          <table className="history-table">
            <thead>
              <tr>
                <th>Patient</th>
                <th>Age</th>
                <th>Gender</th>
                <th>Date</th>
                <th>Prediction</th>
                <th>Confidence</th>
                <th>Model</th>
                <th>Actions</th>
              </tr>
            </thead>

            <tbody>
              {history.map((item) => (
                <tr key={item.id}>
                  <td>
                    <div className="patient-cell">
                      <strong>{item.patient_name || "Unknown Patient"}</strong>

                      {item.clinical_notes && (
                        <small title={item.clinical_notes}>
                          {item.clinical_notes.length > 60
                            ? item.clinical_notes.slice(0, 60) + "..."
                            : item.clinical_notes}
                        </small>
                      )}
                    </div>
                  </td>

                  <td>{item.patient_age ?? "-"}</td>

                  <td>{item.patient_gender || "-"}</td>

                  <td>
                    {item.created_at
                      ? new Date(item.created_at).toLocaleString()
                      : "-"}
                  </td>

                  <td>
                    <span
                      className={`status-tag ${item.prediction?.toLowerCase()}`}
                    >
                      {item.prediction}
                    </span>
                  </td>

                  <td>
                    {item.confidence != null
                      ? `${Number(item.confidence).toFixed(2)}%`
                      : "-"}
                  </td>

                  <td>{item.model || "-"}</td>

                  <td className="actions-cell">
                    <Link to={`/history/${item.id}`} className="btn-view">
                      View
                    </Link>

                    <button
                      type="button"
                      className="btn-delete"
                      onClick={() => handleDelete(item.id)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <footer className="pagination">
        <button
          disabled={page <= 1}
          onClick={() => setPage((prev) => prev - 1)}
        >
          Previous
        </button>

        <span>
          Page <strong>{page}</strong> of{" "}
          <strong>{Math.max(totalPages, 1)}</strong>
        </span>

        <button
          disabled={page >= totalPages || totalPages === 0}
          onClick={() => setPage((prev) => prev + 1)}
        >
          Next
        </button>
      </footer>
    </main>
  );
}

export default History;
