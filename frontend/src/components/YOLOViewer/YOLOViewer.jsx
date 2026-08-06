// YOLOViewer.jsx
import { useRef, useState, useEffect } from "react";
import "./YOLOViewer.css";

function YOLOViewer({ image }) {
  const [loaded, setLoaded] = useState(false);
  const [error, setError] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const modalRef = useRef(null);

  useEffect(() => {
    setLoaded(false);
    setError(false);
  }, [image]);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === "Escape") setShowModal(false);
    };
    if (showModal) {
      window.addEventListener("keydown", handleKeyDown);
      modalRef.current?.focus();
    }
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [showModal]);

  if (!image) {
    return (
      <section
        className="yl-telemetry-card"
        aria-label="Detection output missing fallback"
      >
        <div className="yl-state-indicator fallback-empty" role="alert">
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2.5"
          >
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
            <circle cx="12" cy="12" r="3" />
            <line x1="1" y1="1" x2="23" y2="23" />
          </svg>
          <span>No spatial object localization maps currently computed.</span>
        </div>
      </section>
    );
  }

  const handleDownload = async () => {
    try {
      const response = await fetch(image);
      if (!response.ok) throw new Error("Network stream capture collision.");

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");

      link.href = url;
      link.download = `PneumoAI_Localization_Matrix_${Date.now()}.jpg`;
      document.body.appendChild(link);
      link.click();

      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Pipeline binary payload extraction fault:", err);
    }
  };

  return (
    <>
      <section className="yl-telemetry-card" aria-labelledby="yl-panel-heading">
        <div className="yl-panel-header">
          <div className="yl-header-metadata">
            <h2 id="yl-panel-heading">YOLO Spatial Localization</h2>
            <p>
              Algorithmic bounding overlays highlighting identified spatial
              regions of infiltration.
            </p>
          </div>

          <div className="yl-action-harness">
            <button
              className="yl-trigger-secondary"
              onClick={() => setShowModal(true)}
              type="button"
              disabled={!loaded || error}
              aria-label="Expand localized matrix view into absolute fullscreen view portal"
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
              className="yl-trigger-primary"
              onClick={handleDownload}
              type="button"
              disabled={!loaded || error}
              aria-label="Export mapped graphic coordinates to local disk"
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

        <div className="yl-display-canvas">
          {!loaded && !error && (
            <div className="yl-state-indicator" role="status">
              <div className="yl-inline-spinner"></div>
              <p>Parsing spatial coordinate maps...</p>
            </div>
          )}

          {error && (
            <div className="yl-state-indicator fallback-danger" role="alert">
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2.5"
              >
                <polygon points="7.86 2 16.14 2 22 7.86 22 16.14 16.14 22 7.86 22 2 16.14 2 7.86 7.86 2" />
                <line x1="12" y1="8" x2="12" y2="12" />
                <line x1="12" y1="16" x2="12.01" y2="16" />
              </svg>
              <p>Exception raised mapping coordinate array projection files.</p>
            </div>
          )}

          <img
            src={image}
            alt="YOLO Neural Spatial Object Segmentation matrix"
            crossOrigin="anonymous"
            className={`yl-rendered-matrix ${loaded ? "is-active" : ""}`}
            onLoad={() => setLoaded(true)}
            onError={() => setError(true)}
          />
        </div>
      </section>

      {showModal && (
        <div
          className="yl-overlay-dialog"
          onClick={() => setShowModal(false)}
          role="dialog"
          aria-modal="true"
          aria-label="High-resolution spatial layer view portal"
          ref={modalRef}
          tabIndex={-1}
        >
          <div
            className="yl-dialog-viewport"
            onClick={(e) => e.stopPropagation()}
          >
            <button
              className="yl-overlay-dismiss"
              onClick={() => setShowModal(false)}
              type="button"
              aria-label="Dismiss fullscreen overlay context"
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

            <div className="yl-dialog-frame">
              <img
                src={image}
                alt="High-resolution localized layer view window"
                className="yl-dialog-matrix"
              />
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default YOLOViewer;
