import { useState } from "react";
import { sendChatMessage } from "../services/chatbotService";

export default function useChatbot(predictionId) {
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Hello! I can explain your pneumonia prediction, Grad-CAM visualization, confidence score, and answer medical questions related to this report.",
    },
  ]);

  const [loading, setLoading] = useState(false);

  const askQuestion = async (question) => {
    if (!question.trim()) return;

    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: question,
      },
    ]);

    setLoading(true);

    try {
      const data = await sendChatMessage(predictionId, question);

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: data.answer,
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "Unable to connect with AI assistant.",
        },
      ]);
    }

    setLoading(false);
  };

  return {
    messages,
    loading,
    askQuestion,
  };
}
