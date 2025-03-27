// ✅ New code in GraphPage.js
import React, { useState } from "react";
import axios from "axios";
import GraphVisualization from "./GraphVisualization";

const GraphPage = () => {
  const [graphData, setGraphData] = useState(null);
  const backendBaseUrl = "http://localhost:8000";

  const loadGraphVisualization = async () => {
    try {
      // No 'responseType: "blob"' here. We want JSON.
      const res = await axios.get(`${backendBaseUrl}/visualize-graph`);
      setGraphData(res.data); 
      // res.data is expected to have { nodes: [...], edges: [...] }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <h1>Interactive Graph Visualization</h1>
      <button onClick={loadGraphVisualization}>
        Load Graph Visualization
      </button>
      {graphData && <GraphVisualization graphData={graphData} />}
    </div>
  );
};

export default GraphPage;
