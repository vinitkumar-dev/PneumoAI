// ConfidenceBar.jsx
import { useEffect, useState } from "react";
import "./ConfidenceBar.css";

function ConfidenceBar({ confidence = 0 }) {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const targetValue = Math.min(Math.max(Number(confidence) || 0, 0), 100);
    const animationFrame = requestAnimationFrame(() => {
      setProgress(targetValue);
    });

    return () => cancelAnimationFrame(animationFrame);
  }, [confidence]);

  const getStatus = () => {
    if (confidence >= 95) {
      return {
        color: "excellent",
        label: "Very High Confidence",
        indicator: "◆",
      };
    }
    if (confidence >= 80) {
      return {
        color: "good",
        label: "High Confidence",
        indicator: "▲",
      };
    }
    if (confidence >= 60) {
      return {
        color: "medium",
        label: "Moderate Confidence",
        indicator: "●",
      };
    }
    return {
      color: "low",
      label: "Low Confidence",
      indicator: "■",
    };
  };

  const status = getStatus();

  return (
    <section className="confidence-card" aria-labelledby="confidence-title">
      <div className="confidence-header">
        <div className="confidence-title-group">
          <svg
            className="confidence-icon"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            aria-hidden="true"
          >
            <path
              d="M9 12L11 14L15 10M12 3L3 7V12C3 16.5517 7.04348 20.2526 12 21C16.9565 20.2526 21 16.5517 21 12V7L12 3Z"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          <h3 id="confidence-title">AI Confidence Score</h3>
        </div>
        <span className={`confidence-badge ${status.color}`} role="status">
          <span className="badge-marker" aria-hidden="true">
            {status.indicator}
          </span>
          {status.label}
        </span>
      </div>

      <div className="meter-track-wrapper">
        <div
          className="progress-container"
          role="progressbar"
          aria-valuenow={progress}
          aria-valuemin={0}
          aria-valuemax={100}
          aria-label="Model certainty calculation"
        >
          <div
            className={`progress-fill ${status.color}`}
            style={{ width: `${progress}%` }}
          >
            <div className="progress-glow" aria-hidden="true" />
          </div>
        </div>
      </div>

      <div className="confidence-footer">
        <span className={`current-value ${status.color}`}>
          {Number(progress).toFixed(2)}%
        </span>
        <span className="max-value">100.00% Target</span>
      </div>

      <div className="confidence-note-box">
        <svg
          className="note-icon"
          width="14"
          height="14"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          aria-hidden="true"
        >
          <path
            d="M12 16V12M12 8H12.01M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 17.5228 22 12Z"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
        <p className="confidence-note">
          The confidence metric evaluates deep learning alignment bounds
          relative to validation paradigms. It operates as an interpretive aid
          and must not supersede direct clinical diagnosis.
        </p>
      </div>
    </section>
  );
}

export default ConfidenceBar;
