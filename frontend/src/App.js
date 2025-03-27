// frontend/src/App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navigation from "./components/Navigation";
import HomePage from "./pages/HomePage";
import BalanceSheetPage from "./pages/BalanceSheetPage";
import GraphPage from "./pages/GraphPage";
import ChatPage from "./pages/ChatPage";

function App() {
  return (
    <Router>
      <div className="App" style={{ padding: "20px" }}>
        <Navigation />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/balance-sheet" element={<BalanceSheetPage />} />
          <Route path="/graph" element={<GraphPage />} />
          <Route path="/chat" element={<ChatPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
