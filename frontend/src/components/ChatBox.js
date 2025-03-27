// frontend/src/components/ChatBox.js
import React, { useState } from "react";
import axios from "axios";

const ChatBox = ({ endpoint }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const backendBaseUrl = "http://localhost:8000";

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "Vous", text: input };
    setMessages((prev) => [...prev, userMessage]);

    try {
      // Envoyer la question dans le payload de la requête POST
      const res = await axios.post(`${backendBaseUrl}/${endpoint}`, { question: input });
      // Récupérer la réponse en fonction de l'endpoint appelé
      const responseText =
        res.data[endpoint] || res.data.classic_analysis || res.data.graph_analysis;
      const botMessage = { sender: "Bot", text: responseText };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      console.error(err);
      const errorMsg = { sender: "Bot", text: "Erreur lors de la récupération de la réponse." };
      setMessages((prev) => [...prev, errorMsg]);
    }

    setInput("");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div>
      <div style={{ maxHeight: "300px", overflowY: "auto", marginBottom: "10px", border: "1px solid #ddd", padding: "10px", borderRadius: "4px" }}>
        {messages.map((msg, index) => (
          <div key={index} style={{ marginBottom: "5px" }}>
            <strong>{msg.sender}:</strong> {msg.text}
          </div>
        ))}
      </div>
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        rows="2"
        style={{ width: "100%", padding: "5px", resize: "none" }}
        placeholder="Tapez votre question ici..."
      />
      <button onClick={sendMessage} style={{ marginTop: "5px" }}>
        Envoyer
      </button>
    </div>
  );
};

export default ChatBox;
