// frontend/src/components/Navigation.js
import React from "react";
import { Link } from "react-router-dom";

const Navigation = () => {
  return (
    <nav style={{ marginBottom: "20px" }}>
      <Link to="/" style={{ marginRight: "10px" }}>Home</Link>
      <Link to="/balance-sheet" style={{ marginRight: "10px" }}>Generate Balance Sheet</Link>
      <Link to="/graph" style={{ marginRight: "10px" }}>Graph</Link>
      <Link to="/chat" style={{ marginRight: "10px" }}>Chat</Link>
      <a href="https://github.com/your-username/your-repo" target="_blank" rel="noopener noreferrer">
        Code on GitHub
      </a>
    </nav>
  );
};

export default Navigation;
