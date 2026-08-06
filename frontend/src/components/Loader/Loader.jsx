// Loader.jsx
import "./Loader.css";

function Loader({ fullScreen = false, message = "Analyzing Chest X-ray..." }) {
  return (
    <div
      className={`loader-container ${fullScreen ? "fullscreen" : ""}`}
      role="status"
      aria-live="polite"
      aria-busy="true"
    >
      <div className="medical-loader-wrapper">
        <div className="loader-ring" aria-hidden="true"></div>
        <div className="loader-pulse-core" aria-hidden="true">
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M12 4V20M4 12H20"
              stroke="currentColor"
              strokeWidth="3"
              strokeLinecap="round"
            />
          </svg>
        </div>
      </div>

      <h3 className="loader-title">AI Pneumonia Detection</h3>
      <p className="loader-message">{message}</p>
    </div>
  );
}

export default Loader;
