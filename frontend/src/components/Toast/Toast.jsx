// Toast.jsx
import { useEffect } from "react";
import "./Toast.css";

function Toast({
  type = "success",
  message,
  isOpen,
  onClose,
  duration = 3000,
}) {
  useEffect(() => {
    if (!isOpen) return;

    const timer = setTimeout(() => {
      onClose();
    }, duration);

    return () => clearTimeout(timer);
  }, [isOpen, duration, onClose]);

  if (!isOpen) return null;

  // Accessible Vector Graphics Matrix mapping
  const renderNotificationIcon = (variant) => {
    const baseAttrs = {
      width: "18",
      height: "18",
      viewBox: "0 0 24 24",
      fill: "none",
      stroke: "currentColor",
      strokeWidth: "2.5",
      strokeLinecap: "round",
      strokeLinejoin: "round",
      "aria-hidden": "true",
    };
    switch (variant) {
      case "success":
        return (
          <svg {...baseAttrs}>
            <path d="M22 11.08V12a10 10 0 11-5.93-9.14M22 4L12 14.01l-3-3" />
          </svg>
        );
      case "error":
        return (
          <svg {...baseAttrs}>
            <circle cx="12" cy="12" r="10" />
            <line x1="15" y1="9" x2="9" y2="15" />
            <line x1="9" y1="9" x2="15" y2="15" />
          </svg>
        );
      case "warning":
        return (
          <svg {...baseAttrs}>
            <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0zM12 9v4M12 17h.01" />
          </svg>
        );
      case "info":
        return (
          <svg {...baseAttrs}>
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="16" x2="12" y2="12" />
            <line x1="12" y1="8" x2="12.01" y2="8" />
          </svg>
        );
      default:
        return null;
    }
  };

  return (
    <div
      className={`toast-notification is-${type}`}
      role="status"
      aria-live="polite"
    >
      <div className="toast-payload-group">
        <div className="toast-variant-icon" aria-hidden="true">
          {renderNotificationIcon(type)}
        </div>
        <p className="toast-message-text">{message}</p>
      </div>

      <button
        className="toast-dismiss-action"
        onClick={onClose}
        type="button"
        aria-label="Dismiss real-time alert system notification"
      >
        <svg
          width="14"
          height="14"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2.5"
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden="true"
        >
          <line x1="18" y1="6" x2="6" y2="18" />
          <line x1="6" y1="6" x2="18" y2="18" />
        </svg>
      </button>
    </div>
  );
}

export default Toast;
