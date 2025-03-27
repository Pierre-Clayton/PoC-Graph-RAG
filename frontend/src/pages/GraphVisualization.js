// frontend/src/pages/GraphVisualization.js
import React, { useEffect, useRef } from "react";
import cytoscape from "cytoscape";

const GraphVisualization = ({ graphData }) => {
  const containerRef = useRef(null);
  const cyRef = useRef(null);

  useEffect(() => {
    if (!graphData) return;

    // Build Cytoscape elements from the JSON: map nodes and edges.
    const elements = [
      ...graphData.nodes.map((node) => ({
        data: { id: node.id, label: node.name, type: node.label },
      })),
      ...graphData.edges.map((edge) => ({
        data: {
          source: edge.data.source,
          target: edge.data.target,
          label: edge.data.label,
          // Include additional properties if needed
          ...edge.data,
        },
      })),
    ];

    // Initialize Cytoscape instance
    cyRef.current = cytoscape({
      container: containerRef.current,
      elements: elements,
      style: [
        {
          selector: "node",
          style: {
            "background-color": "#0074D9",
            "label": "data(label)",
            "text-valign": "center",
            "color": "#fff",
            "font-size": "10px",
            "width": "40px",
            "height": "40px",
          },
        },
        {
          selector: "edge",
          style: {
            "width": 2,
            "line-color": "#aaa",
            "target-arrow-color": "#aaa",
            "target-arrow-shape": "triangle",
            "curve-style": "bezier",
            "label": "data(label)",
            "font-size": "8px",
            "text-rotation": "autorotate",
          },
        },
      ],
      layout: {
        name: "cose",
      },
    });

    return () => {
      if (cyRef.current) {
        cyRef.current.destroy();
      }
    };
  }, [graphData]);

  return (
    <div
      ref={containerRef}
      style={{ width: "100%", height: "600px", border: "1px solid #ccc" }}
    />
  );
};

export default GraphVisualization;
