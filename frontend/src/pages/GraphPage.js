// frontend/src/pages/GraphPage.js
import React, { useState } from "react";
import axios from "axios";
import GraphVisualization from "./GraphVisualization";
import "./GraphPage.css";

const GraphPage = () => {
  const [graphData, setGraphData] = useState(null);
  const backendBaseUrl = "http://localhost:8000";

  const loadGraphVisualization = async () => {
    try {
      const res = await axios.get(`${backendBaseUrl}/visualize-graph`);
      setGraphData(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const insertGraphIntoNeo4j = async () => {
    try {
      const res = await axios.post(`${backendBaseUrl}/insert-graph`);
      alert(res.data.status); // Affiche un message de confirmation
    } catch (err) {
      console.error(err);
      alert("Erreur lors de l'insertion du graphe dans Neo4j.");
    }
  };

  return (
    <div className="graph-page-container">
      <h1>Graph Visualization</h1>
      <p>
        Explore the interactive financial knowledge graph generated from BNP Paribas' balance sheet data.
        Click the button below to load the visualization.
      </p>
      <button onClick={loadGraphVisualization} className="primary-button">
        Load Graph Visualization
      </button>
      <button onClick={insertGraphIntoNeo4j} className="primary-button" style={{ marginTop: "10px" }}>
        Insert Graph into Neo4j
      </button>
      {graphData && <GraphVisualization graphData={graphData} />}
    </div>
  );
};

export default GraphPage;
