import React, { useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

const ChatBox = ({ endpoint }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const backendBaseUrl = "http://localhost:8000";

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "You", text: input };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const res = await axios.post(`${backendBaseUrl}/${endpoint}`, { question: input });
      const responseText =
        res.data[endpoint] || res.data.classic_analysis || res.data.graph_analysis;
      const botMessage = { sender: "Bot", text: responseText };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      console.error(err);
      const errorMsg = { sender: "Bot", text: "Error fetching the response." };
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
            <strong>{msg.sender}:</strong>
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {msg.text}
            </ReactMarkdown>
          </div>
        ))}
      </div>
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        rows="2"
        style={{ width: "100%", padding: "5px", resize: "none" }}
        placeholder="Type your question here..."
      />
      <button onClick={sendMessage} style={{ marginTop: "5px" }}>
        Send
      </button>
    </div>
  );
};

export default ChatBox;
