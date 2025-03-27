// frontend/src/pages/ChatPage.js
import React from "react";
import ChatBox from "../components/ChatBox";

const ChatPage = () => {
  return (
    <div>
      <h1>Chat Interactif sur les Données Financières</h1>
      <p>
        Posez vos questions sur les données de bilan. À gauche, obtenez une analyse classique ;
        à droite, une analyse basée sur le graph.
      </p>
      <div style={{ display: "flex", gap: "20px" }}>
        <div style={{ flex: 1, border: "1px solid #ccc", padding: "10px", borderRadius: "4px" }}>
          <h3>Analyse Classique</h3>
          <ChatBox endpoint="classic-analysis" />
        </div>
        <div style={{ flex: 1, border: "1px solid #ccc", padding: "10px", borderRadius: "4px" }}>
          <h3>Analyse Graph</h3>
          <ChatBox endpoint="graph-analysis" />
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
