import api from "./authService";

export const sendChatMessage = async (predictionId, question) => {
  const { data } = await api.post("/api/chat", {
    prediction_id: predictionId,
    question,
  });

  return data;
};
