// Sidebar.jsx
import { NavLink } from "react-router-dom";
import { useState } from "react";
import "./Sidebar.css";

function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);

  const menuItems = [
    { name: "Dashboard", path: "/dashboard", icon: "📊" },
    { name: "Prediction", path: "/prediction", icon: "🩻" },
    { name: "History", path: "/history", icon: "🕒" },
    { name: "Reports", path: "/reports", icon: "📄" },
    { name: "Profile", path: "/profile", icon: "👤" },
  ];

  return (
    <aside className={`sb-nav-container ${collapsed ? "is-collapsed" : ""}`}>
      {/* Structural Control Header */}
      <div className="sb-panel-header">
        {!collapsed && <h3 className="sb-brand-logo">PneumoAI</h3>}

        <button
          className="sb-collapse-trigger"
          onClick={() => setCollapsed((prev) => !prev)}
          aria-label={
            collapsed
              ? "Expand telemetry control drawer"
              : "Collapse telemetry control drawer"
          }
          type="button"
        >
          <svg
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2.5"
          >
            {collapsed ? (
              <path d="M13 5l7 7-7 7M5 5l7 7-7 7" />
            ) : (
              <path d="M11 19l-7-7 7-7M19 19l-7-7 7-7" />
            )}
          </svg>
        </button>
      </div>

      {/* Internal Core Navigation Track */}
      <nav className="sb-menu-track">
        {menuItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `sb-menu-link ${isActive ? "is-active" : ""}`
            }
          >
            <span className="sb-link-icon" aria-hidden="true">
              {item.icon}
            </span>
            {!collapsed && <span className="sb-link-label">{item.name}</span>}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}

export default Sidebar;
