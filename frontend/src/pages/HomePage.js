// frontend/src/pages/HomePage.js
import React from "react";

const HomePage = () => {
  return (
    <div>
      <h1>Bienvenue sur Financial Knowledge Graph App</h1>
      <p>
        Ce projet permet de générer, visualiser et analyser un graph de connaissance
        basé sur les données de bilan de BNP Paribas. L'application utilise une API FastAPI
        pour générer des données financières, créer un graph via OpenAI, et insérer ce graph dans Neo4j.
      </p>
      <h2>Références</h2>
      <ul>
        <li>
          <a href="https://neo4j.com/" target="_blank" rel="noopener noreferrer">
            Neo4j
          </a>
        </li>
        <li>
          <a href="https://fastapi.tiangolo.com/" target="_blank" rel="noopener noreferrer">
            FastAPI
          </a>
        </li>
        <li>
          <a href="https://openai.com/" target="_blank" rel="noopener noreferrer">
            OpenAI
          </a>
        </li>
        <li>
          <a href="https://reactjs.org/" target="_blank" rel="noopener noreferrer">
            React
          </a>
        </li>
      </ul>
    </div>
  );
};

export default HomePage;
