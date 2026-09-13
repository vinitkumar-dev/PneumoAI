// Upload.jsx
import { useRef, useState, useEffect } from "react";
import "./Upload.css";

const ALLOWED_TYPES = ["image/jpeg", "image/jpg", "image/png"];
const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

function Upload({ selectedFile, onFileSelect, disabled = false }) {
  const inputRef = useRef(null);
  const [preview, setPreview] = useState("");
  const [error, setError] = useState("");
  const [isDragging, setIsDragging] = useState(false);

  // =====================================
  // Reactive Image Preview Generation
  // =====================================
  useEffect(() => {
    if (!selectedFile) {
      setPreview("");
      return;
    }

    const imageUrl = URL.createObjectURL(selectedFile);
    setPreview(imageUrl);

    return () => URL.revokeObjectURL(imageUrl);
  }, [selectedFile]);

  // =====================================
  // File Validation Guard Array
  // =====================================
  const validateFile = (file) => {
    if (!file) return false;

    if (!ALLOWED_TYPES.includes(file.type)) {
      setError("Only medical JPG, JPEG, and PNG image arrays are accepted.");
      return false;
    }

    if (file.size > MAX_FILE_SIZE) {
      setError("Maximum permissible medical image payload size is 10 MB.");
      return false;
    }

    setError("");
    return true;
  };

  // =====================================
  // Pipeline Event Ingestion Matrix
  // =====================================
  const handleFile = (file) => {
    if (!file) return;
    if (!validateFile(file)) return;

    if (typeof onFileSelect === "function") {
      onFileSelect(file);
    } else {
      console.warn("Upload: onFileSelect callback listener is missing.");
    }
  };

  const handleInputChange = (event) => {
    const file = event.target.files?.[0];
    handleFile(file);
  };

  const handleDragOver = (event) => {
    event.preventDefault();
    if (!disabled) setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setIsDragging(false);

    if (disabled) return;

    const file = event.dataTransfer.files?.[0];
    handleFile(file);
  };

  const removeImage = (e) => {
    e.stopPropagation(); // Avoid triggering file chooser dialog container
    if (typeof onFileSelect === "function") {
      onFileSelect(null);
    }
    if (inputRef.current) {
      inputRef.current.value = "";
    }
    setPreview("");
    setError("");
  };

  return (
    <div className="upload-wrapper">
      <div
        className={`upload-box ${disabled ? "is-disabled" : ""} ${
          isDragging ? "is-dragging" : ""
        } ${preview ? "has-preview" : ""}`}
        onClick={() => !disabled && inputRef.current?.click()}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        role="button"
        tabIndex={disabled ? -1 : 0}
        aria-label="Upload DICOM or Chest X-ray image array"
        onKeyDown={(e) => {
          if (!disabled && (e.key === "Enter" || e.key === " ")) {
            inputRef.current?.click();
          }
        }}
      >
        {!preview ? (
          <div className="upload-prompt-view">
            <div className="upload-vector-icon" aria-hidden="true">
              <svg
                width="32"
                height="32"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M17 8l-5-5-5 5M12 3v12" />
              </svg>
            </div>
            <h3>Ingest Chest X-ray</h3>
            <p>Drag & drop target DICOM export file here</p>
            <span className="browse-badge">or click to browse filesystem</span>
          </div>
        ) : (
          <div className="upload-preview-wrapper">
            <img
              src={preview}
              alt="Chest X-ray Matrix Preview"
              className="preview-image"
            />
            <div className="preview-overlay-shield">
              <span className="overlay-badge">Click panel to change image</span>
            </div>
          </div>
        )}

        <input
          ref={inputRef}
          type="file"
          accept=".jpg,.jpeg,.png"
          hidden
          onChange={handleInputChange}
          disabled={disabled}
        />
      </div>

      {/* Structured Diagnostics Metadata Panel */}
      {selectedFile && (
        <div className="file-info-panel">
          <div className="file-meta-data-group">
            <svg
              className="file-icon"
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
              <polyline points="14 2 14 8 20 8" />
            </svg>
            <div className="text-truncate-block">
              <strong className="file-name-token">{selectedFile.name}</strong>
              <p className="file-size-token">
                {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB
              </p>
            </div>
          </div>

          <button
            className="remove-action-btn"
            onClick={removeImage}
            disabled={disabled}
            type="button"
            aria-label="Remove uploaded image sequence"
          >
            <span>Clear Matrix</span>
          </button>
        </div>
      )}

      {/* Exception Output Message Blocks */}
      {error && (
        <div className="upload-error-banner" role="alert">
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
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="8" x2="12" y2="12" />
            <line x1="12" y1="16" x2="12.01" y2="16" />
          </svg>
          <span>{error}</span>
        </div>
      )}
    </div>
  );
}

export default Upload;
