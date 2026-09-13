import { useEffect, useRef, useState } from "react";
import api from "../../services/authService";
import "./Chatbot.css";

function Chatbot({ predictionId }) {
  // console.log(predictionId);
  const [messages, setMessages] = useState([
    {
      id: "initial-bot",
      sender: "bot",
      text: "Hello! I'm your AI medical assistant. Ask me about your prediction.",
      timestamp: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
    },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const question = input.trim();

    setMessages((prev) => [
      ...prev,
      {
        id: `user-${Date.now()}`,
        sender: "user",
        text: question,
        timestamp: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      },
    ]);

    setInput("");
    setLoading(true);

    try {
      // console.log("Prediction ID:", predictionId);
      // console.log("Access Token:", localStorage.getItem("accessToken"));

      const response = await api.post("/api/chat", {
        prediction_id: predictionId,
        question,
      });

      setMessages((prev) => [
        ...prev,
        {
          id: `bot-${Date.now()}`,
          sender: "bot",
          text: response.data.answer || "No response received from AI.",
          timestamp: new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          }),
        },
      ]);
    } catch (error) {
      console.error(error);

      let message = "Unable to connect to AI server.";

      if (error.response) {
        console.log(error.response.data);
        message =
          error.response.data.message || error.response.data.msg || message;
      }

      setMessages((prev) => [
        ...prev,
        {
          id: `error-${Date.now()}`,
          sender: "bot",
          text: message,
          isError: true,
          timestamp: new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          }),
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="chatbot-card">
      <div className="chatbot-header">
        <h2>AI Clinical Assistant</h2>
      </div>

      <div className="chat-area">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`message-row ${msg.sender} ${msg.isError ? "system-error" : ""}`}
          >
            <div className="message-bubble">{msg.text}</div>
          </div>
        ))}

        {loading && (
          <div className="message-row bot">
            <div className="message-bubble">Thinking...</div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      <div className="chat-input-row">
        <input
          className="chat-field"
          value={input}
          placeholder="Ask anything..."
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault(); // Prevents line breaks or form anomalies
              sendMessage();
            }
          }}
        />

        <button onClick={sendMessage} disabled={loading || !input.trim()}>
          Send
        </button>
      </div>
    </section>
  );
}

export default Chatbot;
