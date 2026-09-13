// LogoutModal.jsx
import { useEffect, useRef } from "react";
import "./LogoutModal.css";

function LogoutModal({ isOpen, onClose, onConfirm }) {
  const modalRef = useRef(null);
  const cancelBtnRef = useRef(null);

  // Keyboard Event Management (Escape to exit, Focus trapping)
  useEffect(() => {
    if (!isOpen) return;

    const handleKeyDown = (e) => {
      if (e.key === "Escape") {
        onClose();
        return;
      }

      if (e.key === "Tab" && modalRef.current) {
        const focusableElements = modalRef.current.querySelectorAll(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])',
        );
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        if (e.shiftKey) {
          if (document.activeElement === firstElement) {
            lastElement.focus();
            e.preventDefault();
          }
        } else {
          if (document.activeElement === lastElement) {
            firstElement.focus();
            e.preventDefault();
          }
        }
      }
    };

    // Keep focus inside modal when opened
    if (cancelBtnRef.current) {
      cancelBtnRef.current.focus();
    }

    // Trap viewport scroll background mechanics
    document.body.style.overflow = "hidden";

    window.addEventListener("keydown", handleKeyDown);
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      document.body.style.overflow = "";
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="md-overlay-mask" onClick={onClose} role="presentation">
      <div
        className="md-surface-panel"
        onClick={(e) => e.stopPropagation()}
        ref={modalRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="logout-title"
        aria-describedby="logout-desc"
      >
        {/* Vector Accent Node */}
        <div className="md-icon-canister" aria-hidden="true">
          <svg
            width="22"
            height="22"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2.5"
          >
            <path
              d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </div>

        <h2 id="logout-title">Confirm Logout</h2>
        <p id="logout-desc">
          You are about to terminate your active dashboard session. You will
          need to log back in to access patient records.
        </p>

        <div className="md-actions-row">
          <button
            className="md-btn md-btn-secondary"
            onClick={onClose}
            ref={cancelBtnRef}
            type="button"
          >
            Cancel
          </button>

          <button
            className="md-btn md-btn-destructive"
            onClick={onConfirm}
            type="button"
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  );
}

export default LogoutModal;
