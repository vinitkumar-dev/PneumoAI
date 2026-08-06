// PredictionCard.jsx
import "./PredictionCard.css";

function PredictionCard({ predictionData }) {
  if (!predictionData) return null;

  const {
    prediction,
    confidence,
    inference_time,
    explanation,
    classification = {},
  } = predictionData;

  const model = classification.model || "-";
  const isPneumonia = prediction?.toLowerCase() === "pneumonia";

  return (
    <section className="prediction-card" aria-labelledby="prediction-heading">
      {/* Header Matrix Block */}
      <div className="prediction-header">
        <div
          className={`prediction-status-indicator ${
            isPneumonia ? "is-danger" : "is-safe"
          }`}
          aria-hidden="true"
        >
          {isPneumonia ? (
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M12 9v4m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                stroke="currentColor"
                strokeWidth="2.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          ) : (
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M22 11.08V12a10 10 0 11-5.93-9.14M22 4L12 14.01l-3-3"
                stroke="currentColor"
                strokeWidth="2.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          )}
        </div>

        <div className="prediction-title-group">
          <h2 id="prediction-heading">{prediction}</h2>
          <span className="prediction-badge" role="status">
            AI Assisted Classification
          </span>
        </div>
      </div>

      {/* Structured Telemetry Data Field Grid */}
      <div className="prediction-grid">
        <div className="prediction-item">
          <span className="item-label">Confidence Score</span>
          <p className="item-value">
            {confidence != null ? `${confidence}%` : "-"}
          </p>
        </div>

        <div className="prediction-item">
          <span className="item-label">Neural Architecture</span>
          <p className="item-value models-token-truncate">{model}</p>
        </div>

        <div className="prediction-item">
          <span className="item-label">Inference Latency</span>
          <p className="item-value">
            {inference_time != null ? `${inference_time} ms` : "-"}
          </p>
        </div>
      </div>

      {/* Clinical Descriptive Explanation Field */}
      <div className="explanation-card">
        <div className="explanation-header-node">
          <svg
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2.5"
            strokeLinecap="round"
            strokeLinejoin="round"
            aria-hidden="true"
          >
            <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
            <polyline points="14 2 14 8 20 8" />
            <line x1="16" y1="13" x2="8" y2="13" />
            <line x1="16" y1="17" x2="8" y2="17" />
            <polyline points="10 9 9 9 8 9" />
          </svg>
          <h4>Explainable Medical Report</h4>
        </div>
        <p className="explanation-text-payload">{explanation}</p>
      </div>
    </section>
  );
}

export default PredictionCard;
