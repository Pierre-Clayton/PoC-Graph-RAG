// frontend/src/pages/ChatPage.js
import React from "react";
import ChatBox from "../components/ChatBox";

const ChatPage = () => {
  return (
    <div>
      <h1>Interactive Financial Data Chat</h1>
      <p>
        Ask your questions about the balance sheet data. On the left, get a classic analysis;
        on the right, a graph-based analysis.
      </p>
      <div style={{ display: "flex", gap: "20px" }}>
        <div style={{ flex: 1, border: "1px solid #ccc", padding: "10px", borderRadius: "4px" }}>
          <h3>Classic Analysis</h3>
          <ChatBox endpoint="classic-analysis" />
        </div>
        <div style={{ flex: 1, border: "1px solid #ccc", padding: "10px", borderRadius: "4px" }}>
          <h3>Graph Analysis</h3>
          <ChatBox endpoint="graph-analysis" />
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
