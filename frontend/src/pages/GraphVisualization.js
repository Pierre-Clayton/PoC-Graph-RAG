import React from "react";

const GraphVisualization = ({ imageUrl }) => {
  return (
    <div style={{ marginTop: "10px" }}>
      <h3>Visualisation du Graph</h3>
      <img src={imageUrl} alt="Graph Visualization" style={{ maxWidth: "100%", border: "1px solid #ccc" }} />
    </div>
  );
};

export default GraphVisualization;
