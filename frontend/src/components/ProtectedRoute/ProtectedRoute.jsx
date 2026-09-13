import { Navigate, Outlet, useLocation } from "react-router-dom";
import useAuth from "../../hooks/useAuth";
import Loader from "../Loader/Loader";

function ProtectedRoute() {
  const { isAuthenticated, loading } = useAuth();
  const location = useLocation();

  // prevent early redirect flicker
  if (loading) {
    return <Loader text="Checking authentication..." />;
  }

  const token = localStorage.getItem("accessToken");

  if (!isAuthenticated && !token) {
    return (
      <Navigate
        to="/login"
        replace
        state={{ from: location }}
      />
    );
  }

  return <Outlet />;
}
export default ProtectedRoute;