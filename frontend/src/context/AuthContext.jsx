import { createContext, useEffect, useState } from "react";
import {
  login as loginApi,
  logout as logoutApi,
  getCurrentUser,
} from "../services/authService";

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem("user");
    return saved ? JSON.parse(saved) : null;
  });

  const [loading, setLoading] = useState(true);

  const [token, setToken] = useState(
    () => localStorage.getItem("accessToken")
  );

  // Restore session
  useEffect(() => {
    async function loadUser() {
      if (!token) {
        setUser(null);
        setLoading(false);
        return;
      }

      try {
        const response = await getCurrentUser();

        // response = { status: "...", user: {...} }
        setUser(response.user);

        localStorage.setItem(
          "user",
          JSON.stringify(response.user)
        );
      } catch (err) {
        console.error(err);

        localStorage.removeItem("accessToken");
        localStorage.removeItem("user");

        setUser(null);
        setToken(null);
      } finally {
        setLoading(false);
      }
    }

    loadUser();
  }, [token]);

  // Login
  async function login(credentials) {
    const data = await loginApi(credentials);

    // loginApi already stores token in localStorage
    setToken(data.access_token);
    setUser(data.user);

    return data;
  }

  // Logout
  function logout() {
    logoutApi();

    setUser(null);
    setToken(null);
  }

  const isAuthenticated = !!token;

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,
        login,
        logout,
        isAuthenticated,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}