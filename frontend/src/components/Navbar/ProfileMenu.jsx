// ProfileMenu.jsx
import { useState, useRef, useEffect } from "react";
import "./ProfileMenu.css";

function ProfileMenu({ user, initials, onLogout, onNavigate }) {
  const [open, setOpen] = useState(false);
  const menuRef = useRef();

  // Handle click outside to close the dropdown menu
  useEffect(() => {
    const handler = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setOpen(false);
      }
    };

    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  // Handle global escape key down events for accessibility
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === "Escape") setOpen(false);
    };
    if (open) {
      window.addEventListener("keydown", handleKeyDown);
    }
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [open]);

  const handleItemClick = (path) => {
    onNavigate(path);
    setOpen(false);
  };

  return (
    <div className="profile-container" ref={menuRef}>
      {/* Interactive Trigger Button */}
      <button
        className={`avatar-trigger ${open ? "is-active" : ""}`}
        onClick={() => setOpen(!open)}
        type="button"
        aria-haspopup="true"
        aria-expanded={open}
        aria-label="Toggle user profile menu matrix"
      >
        <span className="avatar-text-node">{initials}</span>
      </button>

      {/* Floating Action Menu Panel */}
      {open && (
        <div
          className="dropdown-panel"
          role="menu"
          aria-label="User Account Options"
        >
          <div className="user-profile-summary">
            <div className="avatar-display-large" aria-hidden="true">
              {initials}
            </div>
            <div className="user-metadata-block">
              <h4>{user?.name || "Medical Officer"}</h4>
              <p>{user?.email || "session@pneumoai.local"}</p>
            </div>
          </div>

          <div className="dropdown-divider" role="separator" />

          <button
            className="menu-item-action"
            onClick={() => handleItemClick("/dashboard")}
            role="menuitem"
            type="button"
          >
            <svg
              className="menu-action-icon"
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
              <rect x="3" y="3" width="18" height="18" rx="2" />
              <path d="M9 3v18M15 3v18M3 9h18M3 15h18" />
            </svg>
            <span>Dashboard</span>
          </button>

          <button
            className="menu-item-action"
            onClick={() => handleItemClick("/history")}
            role="menuitem"
            type="button"
          >
            <svg
              className="menu-action-icon"
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
              <path d="M12 8v4l3 3" />
              <circle cx="12" cy="12" r="9" />
            </svg>
            <span>History</span>
          </button>

          <div className="dropdown-divider" role="separator" />

          <button
            className="menu-item-action destructive-logout"
            onClick={() => {
              setOpen(false);
              onLogout();
            }}
            role="menuitem"
            type="button"
          >
            <svg
              className="menu-action-icon"
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
              <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9" />
            </svg>
            <span>Logout</span>
          </button>
        </div>
      )}
    </div>
  );
}

export default ProfileMenu;
