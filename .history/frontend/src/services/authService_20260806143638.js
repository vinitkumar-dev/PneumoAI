import axios from "axios";

// =====================================================
// BACKEND URL
// =====================================================
const BASE_URL =
  import.meta.env.VITE_API_URL || "https://pneumoai-hgh9.onrender.com";

// =====================================================
// AXIOS INSTANCE
// =====================================================
const api = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

// =====================================================
// REQUEST INTERCEPTOR
// =====================================================
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("accessToken");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error),
);

// =====================================================
// RESPONSE INTERCEPTOR
// =====================================================
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("accessToken");
      localStorage.removeItem("user");

      window.location.href = "/login";
    }

    return Promise.reject(error);
  },
);

// =====================================================
// AUTH APIs
// =====================================================
export const register = async (data) => {
  const response = await api.post("/auth/register", data);
  return response.data;
};

export const login = async (data) => {
  const response = await api.post("/auth/login", data);

  localStorage.setItem("accessToken", response.data.access_token);

  localStorage.setItem("user", JSON.stringify(response.data.user));

  return response.data;
};

export const logout = () => {
  localStorage.removeItem("accessToken");
  localStorage.removeItem("user");
};

export const getCurrentUser = async () => {
  const response = await api.get("/auth/me");
  return response.data;
};

// =====================================================
// PREDICTION APIs
// =====================================================
export const predictImage = async (formData) => {
  const response = await api.post("/predict", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};

// =====================================================
// DASHBOARD
// =====================================================
export const getDashboard = async () => {
  const response = await api.get("/dashboard");
  return response.data;
};

// =====================================================
// HISTORY
// =====================================================
export const getHistory = async () => {
  const response = await api.get("/history");
  return response.data;
};

// =====================================================
// CHAT
// =====================================================
export const sendChatMessage = async (message) => {
  const response = await api.post("/chat", {
    message,
  });

  return response.data;
};

// =====================================================
// REPORT
// =====================================================
export const downloadReport = async (id) => {
  const response = await api.get(`/report/${id}`, {
    responseType: "blob",
  });

  return response.data;
};

// =====================================================
// HEALTH CHECK
// =====================================================
export const healthCheck = async () => {
  const response = await api.get("/health");
  return response.data;
};

// =====================================================
// HELPERS
// =====================================================
export const getToken = () => localStorage.getItem("accessToken");

export const getUser = () => {
  const user = localStorage.getItem("user");
  return user ? JSON.parse(user) : null;
};

export const isAuthenticated = () => !!localStorage.getItem("accessToken");

export default api;
