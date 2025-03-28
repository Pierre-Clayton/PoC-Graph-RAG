import React from "react";
import ChatBox from "../components/ChatBox";
import "./ChatPage.css";

const ChatPage = () => {
  return (
    <div className="chat-page-container">
      <h1>Financial Data Chat</h1>
      <p className="chat-description">
        Engage with our interactive chat to receive both classic and graph-based analyses of the financial data.
        Ask your questions and get insights instantly.
      </p>
      <div className="chat-boxes">
        <div className="chat-card">
          <h3>Classic Analysis</h3>
          <ChatBox endpoint="classic-analysis" />
        </div>
        <div className="chat-card">
          <h3>Graph Analysis</h3>
          <ChatBox endpoint="graph-analysis" />
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
