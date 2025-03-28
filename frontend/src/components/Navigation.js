import React from "react";
import { Link } from "react-router-dom";
import "./Navigation.css";

const Navigation = () => {
  return (
    <nav className="navigation">
      <Link to="/" className="nav-link">Home</Link>
      <Link to="/balance-sheet" className="nav-link">Balance Sheet</Link>
      <Link to="/graph" className="nav-link">Graph</Link>
      <Link to="/chat" className="nav-link">Chat</Link>
    </nav>
  );
};

export default Navigation;
