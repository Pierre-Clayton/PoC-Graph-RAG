import React from "react";

const Navigation = () => {
  return (
    <nav style={{ marginBottom: "20px" }}>
      <a href="/" style={{ marginRight: "10px" }}>
        Accueil
      </a>
      <a href="https://github.com/votre-utilisateur/votre-repo" target="_blank" rel="noopener noreferrer">
        Code sur GitHub
      </a>
    </nav>
  );
};

export default Navigation;
