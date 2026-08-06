import api from "./authService";

export const getPrediction = async (id) => {
  const response = await api.get(`/api/predictions/${id}`);
  return response.data;
};
