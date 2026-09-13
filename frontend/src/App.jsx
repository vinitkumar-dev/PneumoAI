// App.jsx
import { Routes, Route, Navigate } from "react-router-dom";

// Pages
import Home from "./pages/Home/Home";
import Login from "./pages/Login/Login";
import Register from "./pages/Register/Register";
import Dashboard from "./pages/Dashboard/Dashboard";
import Prediction from "./pages/Prediction/Prediction";
import History from "./pages/History/History";
import PredictionDetails from "./pages/PredictionDetails/PredictionDetails";

// Components
import ProtectedRoute from "./components/ProtectedRoute/ProtectedRoute";

// Layout
import DashboardLayout from "./layouts/DashboardLayout";

// Styling Core Matrix Hook
import "./App.css";

function App() {
  return (
    <Routes>
      {/* ================= Public Routes ================= */}
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      {/* ================= Protected Routes ================= */}
      <Route element={<ProtectedRoute />}>
        <Route element={<DashboardLayout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/prediction" element={<Prediction />} />
          <Route path="/history" element={<History />} />
          <Route path="/history/:id" element={<PredictionDetails />} />
        </Route>
      </Route>

      {/* ================= 404 Fallback Matrix Redirect ================= */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;
