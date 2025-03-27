// frontend/src/components/Navigation.js
import React from "react";
import { Link } from "react-router-dom";

const Navigation = () => {
  return (
    <nav style={{ marginBottom: "20px" }}>
      <Link to="/" style={{ marginRight: "10px" }}>Accueil</Link>
      <Link to="/balance-sheet" style={{ marginRight: "10px" }}>Générer Bilan</Link>
      <Link to="/graph" style={{ marginRight: "10px" }}>Schéma & Graph</Link>
      <Link to="/chat" style={{ marginRight: "10px" }}>Chat</Link>
      <a href="https://github.com/votre-utilisateur/votre-repo" target="_blank" rel="noopener noreferrer">
        Code sur GitHub
      </a>
    </nav>
  );
};

export default Navigation;
