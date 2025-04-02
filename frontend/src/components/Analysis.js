// frontend/src/components/Analysis.js
import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

const Analysis = ({ title, analysis }) => {
  return (
    <div style={{ backgroundColor: "#eef", padding: "10px", marginTop: "10px", borderRadius: "4px" }}>
      <h3>{title}</h3>
      <ReactMarkdown remarkPlugins={[remarkGfm]}>
        {analysis}
      </ReactMarkdown>
    </div>
  );
};

export default Analysis;
