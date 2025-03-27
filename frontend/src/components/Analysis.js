import React from "react";

const Analysis = ({ title, analysis }) => {
  return (
    <div style={{ backgroundColor: "#eef", padding: "10px", marginTop: "10px", borderRadius: "4px" }}>
      <h3>{title}</h3>
      <p>{analysis}</p>
    </div>
  );
};

export default Analysis;
