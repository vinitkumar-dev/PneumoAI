// GradCAMViewer.jsx
import { useState, useEffect } from "react";
import "./GradCAMViewer.css";

function GradCAMViewer({ image }) {
  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageError, setImageError] = useState(false);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    setImageLoaded(false);
    setImageError(false);
  }, [image]);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === "Escape") setShowModal(false);
    };
    if (showModal) {
      window.addEventListener("keydown", handleKeyDown);
    }
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [showModal]);

  if (!image) return null;

  const downloadImage = async () => {
    try {
      const response = await fetch(image);
      if (!response.ok) throw new Error("Failed to fetch spatial map stream.");

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");

      link.href = url;
      link.download = "gradcam-activation-map.jpg";

      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Download pipeline execution failure:", error);
    }
  };

  return (
    <>
      <section
        className="gc-telemetry-card"
        aria-label="Grad-CAM Deep Activation Map"
      >
        <div className="gc-panel-header">
          <div className="gc-header-metadata">
            <h2>Grad-CAM Localization</h2>
            <p>
              Highlights the matrix grids that heavily weighted convolutional
              tensor activation branches.
            </p>
          </div>

          <div className="gc-action-harness">
            <button
              className="gc-trigger-secondary"
              onClick={() => setShowModal(true)}
              type="button"
              disabled={!imageLoaded || imageError}
            >
              <svg
                width="14"
                height="14"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2.5"
              >
                <path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7" />
              </svg>
              <span>Viewport Expand</span>
            </button>

            <button
              className="gc-trigger-primary"
              onClick={downloadImage}
              type="button"
              disabled={!imageLoaded || imageError}
            >
              <svg
                width="14"
                height="14"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2.5"
              >
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v4M7 10l5 5 5-5M12 15V3" />
              </svg>
              <span>Commit Fetch</span>
            </button>
          </div>
        </div>

        <div className="gc-display-canvas">
          {!imageLoaded && !imageError && (
            <div className="gc-state-indicator" role="status">
              <div className="gc-inline-spinner"></div>
              <p>Reconstructing tensor weights...</p>
            </div>
          )}

          {imageError && (
            <div className="gc-state-indicator fallback-danger" role="alert">
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2.5"
              >
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0zM12 9v4M12 17h.01" />
              </svg>
              <p>Activation stream matrix missing.</p>
            </div>
          )}

          <img
            src={image}
            alt="Grad-CAM activation distribution mapping"
            className={`gc-rendered-matrix ${imageLoaded ? "is-active" : ""}`}
            onLoad={() => setImageLoaded(true)}
            onError={() => setImageError(true)}
          />
        </div>
      </section>

      {showModal && (
        <div
          className="gc-overlay-dialog"
          onClick={() => setShowModal(false)}
          role="dialog"
          aria-modal="true"
        >
          <div
            className="gc-dialog-viewport"
            onClick={(e) => e.stopPropagation()}
          >
            <button
              className="gc-overlay-dismiss"
              onClick={() => setShowModal(false)}
              aria-label="Dismiss full spatial viewport overlay"
              type="button"
            >
              <svg
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2.5"
              >
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>

            <div className="gc-dialog-frame">
              <img
                src={image}
                alt="Expanded diagnostic weight distribution overlay detail matrix view"
                className="gc-dialog-matrix"
              />
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default GradCAMViewer;
