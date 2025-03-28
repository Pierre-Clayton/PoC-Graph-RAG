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
      {graphData && <GraphVisualization graphData={graphData} />}
    </div>
  );
};

export default GraphPage;
