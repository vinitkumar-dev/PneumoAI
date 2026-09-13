// Navbar.jsx
import { useState, useContext, useEffect } from "react";
import { useNavigate, NavLink } from "react-router-dom";

import { AuthContext } from "../../context/AuthContext";
import ProfileMenu from "./ProfileMenu";
import LogoutModal from "./LogoutModal";

import "./Navbar.css";

function Navbar() {
  const navigate = useNavigate();
  const { isAuthenticated, user, logout } = useContext(AuthContext);

  const [menuOpen, setMenuOpen] = useState(false);
  const [showLogoutModal, setShowLogoutModal] = useState(false);

  // Parse initials safely
  const initials =
    user?.name
      ?.split(" ")
      .map((n) => n[0])
      .join("")
      .substring(0, 2)
      .toUpperCase() || "U";

  // Prevent background scrolling when mobile navigation drawer is active
  useEffect(() => {
    if (menuOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [menuOpen]);

  const handleLogoutClick = () => {
    setShowLogoutModal(true);
  };

  const confirmLogout = () => {
    logout();
    setShowLogoutModal(false);
    setMenuOpen(false);
    navigate("/login", { replace: true });
  };

  const closeMenu = () => {
    setMenuOpen(false);
  };

  return (
    <header className="navbar">
      <div className="navbar-container">
        {/* Interactive Branding Node */}
        <div
          className="navbar-logo"
          onClick={() => {
            navigate("/");
            closeMenu();
          }}
          role="button"
          tabIndex={0}
          onKeyDown={(e) => {
            if (e.key === "Enter" || e.key === " ") {
              navigate("/");
              closeMenu();
            }
          }}
          aria-label="PneumoAI Home Gateway"
        >
          <svg
            className="navbar-logo-svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            aria-hidden="true"
          >
            <path
              d="M12 4V20M4 12H20M12 4C8.5 4 6 7.5 6 12C6 16.5 8.5 20 12 20M12 4C15.5 4 18 7.5 18 12C18 16.5 15.5 20 12 20"
              stroke="currentColor"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>

          <div className="logo-text-group">
            <h2>PneumoAI</h2>
            <span className="logo-subtitle">AI Medical Dashboard</span>
          </div>
        </div>

        {/* Global Navigation Bus */}
        <nav
          className={`navbar-links ${menuOpen ? "active" : ""}`}
          aria-label="Primary Portal Navigation"
        >
          <NavLink
            to="/"
            onClick={closeMenu}
            className={({ isActive }) =>
              isActive ? "nav-item active" : "nav-item"
            }
          >
            Home
          </NavLink>

          {isAuthenticated && (
            <>
              <NavLink
                to="/dashboard"
                onClick={closeMenu}
                className={({ isActive }) =>
                  isActive ? "nav-item active" : "nav-item"
                }
              >
                Dashboard
              </NavLink>

              <NavLink
                to="/prediction"
                onClick={closeMenu}
                className={({ isActive }) =>
                  isActive ? "nav-item active" : "nav-item"
                }
              >
                Prediction
              </NavLink>

              <NavLink
                to="/history"
                onClick={closeMenu}
                className={({ isActive }) =>
                  isActive ? "nav-item active" : "nav-item"
                }
              >
                History
              </NavLink>
            </>
          )}

          {/* Inline Mobile-only Access Arrays */}
          {!isAuthenticated && (
            <div className="mobile-guest-links">
              <NavLink to="/login" onClick={closeMenu} className="nav-item">
                Login
              </NavLink>
              <NavLink
                to="/register"
                onClick={closeMenu}
                className="nav-item mobile-register-btn"
              >
                Register
              </NavLink>
            </div>
          )}
        </nav>

        {/* Desktop Interface Control Node */}
        <div className="navbar-right">
          {!isAuthenticated && (
            <div className="guest-actions">
              <NavLink to="/login" className="guest-login-link">
                Login
              </NavLink>
              <NavLink to="/register" className="guest-register-btn">
                Register
              </NavLink>
            </div>
          )}

          {isAuthenticated && (
            <ProfileMenu
              user={user}
              initials={initials}
              onLogout={handleLogoutClick}
              onNavigate={(path) => {
                navigate(path);
                closeMenu();
              }}
            />
          )}

          {/* Responsive Layout Toggle Button */}
          <button
            className={`menu-btn ${menuOpen ? "is-open" : ""}`}
            onClick={() => setMenuOpen(!menuOpen)}
            type="button"
            aria-expanded={menuOpen}
            aria-label={
              menuOpen ? "Close navigation tray" : "Open navigation tray"
            }
          >
            {menuOpen ? (
              <svg
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M18 6L6 18M6 6L18 18"
                  stroke="currentColor"
                  strokeWidth="2.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            ) : (
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M3 12h18M3 6h18M3 18h18"
                  stroke="currentColor"
                  strokeWidth="2.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            )}
          </button>
        </div>
      </div>

      {/* Portal Escape Intermediary Layer */}
      <LogoutModal
        isOpen={showLogoutModal}
        onClose={() => setShowLogoutModal(false)}
        onConfirm={confirmLogout}
      />
    </header>
  );
}

export default Navbar;
