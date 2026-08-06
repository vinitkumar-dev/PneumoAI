// Footer.jsx
import { NavLink } from "react-router-dom";
import "./Footer.css";

function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="footer" aria-labelledby="footer-brand-heading">
      <div className="footer-container">
        {/* Brand Section */}
        <div className="footer-section brand-info">
          <div className="footer-logo">
            <svg
              className="logo-svg"
              width="22"
              height="22"
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
            <h2 id="footer-brand-heading">PneumoAI</h2>
          </div>
          <p className="brand-description">
            Advanced clinical imaging nodes processing deep convolutional
            metrics. Utilizing model interpretability architectures via Grad-CAM
            and localization systems to enhance diagnostics.
          </p>
        </div>

        {/* Quick Links */}
        <div className="footer-section links-group">
          <h3>Application</h3>
          <nav className="footer-nav" aria-label="Application links">
            <NavLink
              to="/"
              className={({ isActive }) =>
                isActive ? "footer-link active" : "footer-link"
              }
            >
              Home Gateway
            </NavLink>
            <NavLink
              to="/dashboard"
              className={({ isActive }) =>
                isActive ? "footer-link active" : "footer-link"
              }
            >
              Analysis Desk
            </NavLink>
            <NavLink
              to="/prediction"
              className={({ isActive }) =>
                isActive ? "footer-link active" : "footer-link"
              }
            >
              Engine Execution
            </NavLink>
            <NavLink
              to="/history"
              className={({ isActive }) =>
                isActive ? "footer-link active" : "footer-link"
              }
            >
              Archived Diagnostics
            </NavLink>
          </nav>
        </div>

        {/* Resources */}
        <div className="footer-section links-group">
          <h3>Documentation</h3>
          <nav className="footer-nav" aria-label="Resource links">
            <a href="#docs" className="footer-link">
              Model Whitepapers
            </a>
            <a href="#privacy" className="footer-link">
              Data Privacy Protocols
            </a>
            <a href="#terms" className="footer-link">
              Operational Terms
            </a>
            <a href="#support" className="footer-link">
              Node Support
            </a>
          </nav>
        </div>

        {/* Contact */}
        <div className="footer-section contact-info">
          <h3>Node Registry</h3>

          <div className="contact-item">
            <span className="contact-label">Secure Mail</span>
            <a href="mailto:support@pneumoai.com" className="contact-value">
              support@pneumoai.com
            </a>
          </div>

          <div className="contact-item">
            <span className="contact-label">Facility</span>
            <span className="contact-value">Clinical AI Frameworks Group</span>
          </div>

          <div
            className="footer-social"
            aria-label="Core operational repositories"
          >
            <a
              href="#linkedin"
              aria-label="LinkedIn Profile"
              className="social-icon"
            >
              <svg
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path>
                <rect x="2" y="9" width="4" height="12"></rect>
                <circle cx="4" cy="4" r="2"></circle>
              </svg>
            </a>
            <a
              href="#github"
              aria-label="GitHub Repository"
              className="social-icon"
            >
              <svg
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path>
              </svg>
            </a>
            <a
              href="#twitter"
              aria-label="Twitter Profile"
              className="social-icon"
            >
              <svg
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 11.64 0 0 1-7 2c9 5 20 0 20-11.5a4.5 4.5 0 0 0-.08-.83A7.72 7.72 0 0 0 23 3z"></path>
              </svg>
            </a>
          </div>
        </div>
      </div>

      <div className="footer-bottom">
        <div className="footer-bottom-container">
          <p>© {year} PneumoAI Engineering. Cryptographically verified.</p>
          <span className="compliance-tag">
            HIPAA / GDPR Compliant Data Tunnels
          </span>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
