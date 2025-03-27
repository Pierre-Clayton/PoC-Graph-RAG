// frontend/src/pages/HomePage.js
import React from "react";

const HomePage = () => {
  return (
    <div>
      <h1>Welcome to Financial Knowledge Graph App</h1>
      <p>
        This project allows you to generate, visualize, and analyze a knowledge graph based on BNP Paribas balance sheet data.
        The application uses a FastAPI API to generate financial data, create a graph using OpenAI, and insert this graph into Neo4j.
      </p>
      <h2>References</h2>
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
