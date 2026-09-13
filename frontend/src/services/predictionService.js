// predictionService.js
import api from "./authService";

export const predictPneumonia = async (formData) => {
  const response = await api.post("/predict", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
    // 🔥 THE FIX: Override the global timeout for this heavy inference request
    // Set to 120,000 milliseconds (2 minutes) to give the AI time to process
    timeout: 120000,
  });

  return response.data;
};
