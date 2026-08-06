// Hero.jsx
import { Link } from "react-router-dom";
import "./Hero.css";

function Hero() {
  return (
    <section className="hero" aria-labelledby="hero-heading">
      <div className="hero-blur-backdrop" aria-hidden="true">
        <div className="hero-orb hero-orb-1"></div>
        <div className="hero-orb hero-orb-2"></div>
      </div>

      <div className="hero-container">
        {/* Left Column: Copy & Core Data Matrices */}
        <div className="hero-content">
          <span className="hero-badge" role="status">
            <svg
              width="12"
              height="12"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              aria-hidden="true"
            >
              <path
                d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"
                stroke="currentColor"
                strokeWidth="2.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            AI-Powered Medical Imaging
          </span>

          <h1 id="hero-heading">
            Early Pneumonia Detection Using
            <span className="hero-highlight"> Deep Learning & YOLO</span>
          </h1>

          <p className="hero-description">
            Upload a chest X-ray and receive an AI-assisted diagnosis with
            confidence score, Grad-CAM visualization, YOLO localization, model
            performance metrics, and an explainable medical report.
          </p>

          <div className="hero-buttons">
            <Link to="/prediction" className="hero-btn h-primary-btn">
              <span>Start Diagnosis</span>
              <svg
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                aria-hidden="true"
              >
                <path
                  d="M5 12H19M19 12L13 6M19 12L13 18"
                  stroke="currentColor"
                  strokeWidth="2.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </Link>

            <Link to="/dashboard" className="hero-btn h-secondary-btn">
              <span>View Dashboard</span>
            </Link>
          </div>

          <div className="hero-stats">
            <div className="stat-card">
              <div className="stat-inner-glow" aria-hidden="true" />
              <h2>90.5%</h2>
              <span>Validation Accuracy</span>
            </div>

            <div className="stat-card">
              <div className="stat-inner-glow" aria-hidden="true" />
              <h2>0.38s</h2>
              <span>Inference Speed</span>
            </div>

            <div className="stat-card">
              <div className="stat-inner-glow" aria-hidden="true" />
              <h2>24/7</h2>
              <span>Node Availability</span>
            </div>
          </div>
        </div>

        {/* Right Column: Visualization Graphics Block */}
        <div className="hero-image-pane">
          <div className="scan-card">
            <div className="scan-header">
              <div className="scan-status-dot" aria-hidden="true"></div>
              <span>Neural Pipeline Monitor</span>
            </div>

            <div className="scan-body">
              <div className="scan-viewport-wrapper">
                <div
                  className="scan-placeholder"
                  role="img"
                  aria-label="Anatomical X-ray projection simulation"
                >
                  <svg
                    className="xray-placeholder-svg"
                    width="64"
                    height="64"
                    viewBox="0 0 24 24"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M4 3h16a1 1 0 011 1v16a1 1 0 01-1 1H4a1 1 0 01-1-1V4a1 1 0 011-1zm8 4v10M8 9h8M8 12h8M8 15h8"
                      stroke="currentColor"
                      strokeWidth="1.5"
                      strokeLinecap="round"
                    />
                  </svg>
                </div>
                <div className="scan-laser-line" aria-hidden="true"></div>
              </div>

              <div className="scan-result success" role="status">
                <span className="engine-tag">EfficientNet-B0</span>
                <span className="result-metric">Confidence 97.64%</span>
              </div>

              <div className="scan-progress-track" aria-hidden="true">
                <div className="scan-progress-fill"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default Hero;
