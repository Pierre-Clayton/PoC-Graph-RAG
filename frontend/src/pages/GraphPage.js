// frontend/src/pages/GraphPage.js
import React, { useState } from "react";
import axios from "axios";

const GraphPage = () => {
  const [graphJson, setGraphJson] = useState("");
  const [graphImage, setGraphImage] = useState(null);
  const backendBaseUrl = "http://localhost:8000";

  const generateGraphJson = async () => {
    try {
      const res = await axios.post(`${backendBaseUrl}/generate-graph-json`);
      setGraphJson(JSON.stringify(res.data, null, 2));
    } catch (err) {
      console.error(err);
    }
  };

  const getGraphVisualization = async () => {
    try {
      const res = await axios.get(`${backendBaseUrl}/visualize-graph`, { responseType: "blob" });
      const imageUrl = URL.createObjectURL(res.data);
      setGraphImage(imageUrl);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <h1>JSON Schema and Graph Visualization</h1>
      <div style={{ marginBottom: "20px" }}>
        <button onClick={generateGraphJson}>Generate Graph JSON</button>
        {graphJson && (
          <pre style={{ backgroundColor: "#f4f4f4", padding: "10px", overflow: "auto", marginTop: "10px" }}>
            {graphJson}
          </pre>
        )}
      </div>
      <div>
        <button onClick={getGraphVisualization}>Visualize Graph</button>
        {graphImage && (
          <div style={{ marginTop: "10px" }}>
            <h3>Graph Visualization</h3>
            <img src={graphImage} alt="Graph Visualization" style={{ maxWidth: "100%", border: "1px solid #ccc" }} />
          </div>
        )}
      </div>
    </div>
  );
};

export default GraphPage;
