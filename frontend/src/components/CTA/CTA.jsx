// CTA.jsx
import { useNavigate } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "../../context/AuthContext";
import "./CTA.css";

function CTA({
  title = "Start Your AI-Powered Pneumonia Screening Today",
  description = "Upload a chest X-ray and receive an explainable AI prediction with Grad-CAM visualization, YOLO detection, confidence score, performance metrics, and a downloadable medical report.",
}) {
  const navigate = useNavigate();
  const { isAuthenticated } = useContext(AuthContext);

  const handlePrimaryAction = () => {
    if (isAuthenticated) {
      navigate("/dashboard");
    } else {
      navigate("/register");
    }
  };

  const handleSecondaryAction = () => {
    if (isAuthenticated) {
      navigate("/history");
    } else {
      navigate("/login");
    }
  };

  return (
    <section className="cta-section" aria-labelledby="cta-heading">
      <div className="cta-blur-backdrop" aria-hidden="true">
        <div className="cta-orb cta-orb-1"></div>
        <div className="cta-orb cta-orb-2"></div>
      </div>

      <div className="cta-container">
        <div className="cta-card">
          <div className="cta-content-wrapper">
            <span className="cta-badge" role="status">
              <svg
                width="12"
                height="12"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                aria-hidden="true"
              >
                <path
                  d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 2 12 22Z"
                  stroke="currentColor"
                  strokeWidth="2.5"
                />
                <path
                  d="M12 6V12L16 14"
                  stroke="currentColor"
                  strokeWidth="2.5"
                  strokeLinecap="round"
                />
              </svg>
              AI Healthcare Platform
            </span>

            <h2 id="cta-heading">{title}</h2>
            <p>{description}</p>

            <div className="cta-buttons">
              <button
                className="cta-primary-btn"
                onClick={handlePrimaryAction}
                type="button"
              >
                <span>
                  {isAuthenticated ? "Go to Dashboard" : "Get Started Now"}
                </span>
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
              </button>

              <button
                className="cta-secondary-btn"
                onClick={handleSecondaryAction}
                type="button"
              >
                <span>
                  {isAuthenticated ? "View History" : "Sign In to Portal"}
                </span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default CTA;
