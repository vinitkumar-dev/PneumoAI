// DashboardLayout.jsx
import { Outlet } from "react-router-dom";
import Navbar from "../components/Navbar/Navbar";
// import Sidebar from "../components/Sidebar/Sidebar";
import "./DashboardLayout.css";

function DashboardLayout() {
  return (
    <div className="ly-app-shell">
      <Navbar />

      <div className="ly-viewport-canvas">
        {/* <Sidebar /> */}

        <main className="ly-content-stage" id="main-content" role="main">
          <div className="ly-scroll-wrapper">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}

export default DashboardLayout;
