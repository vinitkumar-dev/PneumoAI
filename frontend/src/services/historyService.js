import api from "./authService";

export async function getPredictionHistory(params = {}) {
  const {
    page = 1,
    search = "",
    prediction = "",
  } = params;

  const { data } = await api.get("/api/predictions/history", {
    params: {
      page,
      search,
      prediction,
    },
  });

  return data;
}

export async function deletePrediction(id) {
  const { data } = await api.delete(`/api/predictions/${id}`);
  return data;
}

export async function getPredictionDetails(id) {
  const { data } = await api.get(`/api/predictions/${id}`);
  return data;
}