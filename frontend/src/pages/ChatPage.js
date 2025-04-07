// frontend/src/pages/ChatPage.js
import React from "react";
import ChatBox from "../components/ChatBox";
import "./ChatPage.css";

const ChatPage = () => {
  return (
    <div className="chat-page-container">
      <h1>Financial Data Chat</h1>
      <p className="chat-description">
        Engage with our interactive chat to receive both classic and graph-based analyses of the financial data. Ask your questions and get insights instantly.
        "Make a complete financial analysis of BNP Paribas through the periods"      </p>
      <div className="chat-boxes">
        <div className="chat-card">
          <h3>Classic Analysis</h3>
          <div className="chat-box-container">
            <ChatBox endpoint="classic-analysis" />
          </div>
        </div>
        <div className="chat-card">
          <h3>Graph Analysis</h3>
          <div className="chat-box-container">
            <ChatBox endpoint="graph-analysis" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
