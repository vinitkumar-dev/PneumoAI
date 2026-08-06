import api from "./authService";

export const getDashboardSummary = async () => {
  const { data } = await api.get("/api/dashboard/summary");
  return data;
};

export const getRecentPredictions = async () => {
  const { data } = await api.get("/api/predictions/history?page=1");

  // Adjust depending on history response
  if (data.items) return data.items.slice(0, 5);
  if (data.predictions) return data.predictions.slice(0, 5);
  if (Array.isArray(data)) return data.slice(0, 5);

  return [];
};

export const deletePrediction = async (id) => {
  const { data } = await api.delete(`/api/predictions/${id}`);
  return data;
};