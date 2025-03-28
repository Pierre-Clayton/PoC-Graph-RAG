import React, { useEffect, useRef } from "react";
import cytoscape from "cytoscape";
import "./GraphVisualization.css";

const GraphVisualization = ({ graphData }) => {
  const containerRef = useRef(null);
  const cyRef = useRef(null);

  useEffect(() => {
    if (!graphData) return;

    const elements = [
      ...graphData.nodes.map((node) => ({
        data: { id: node.id, label: node.name, type: node.label },
      })),
      ...graphData.edges.map((edge) => ({
        data: {
          source: edge.data.source,
          target: edge.data.target,
          label: edge.data.label,
          ...edge.data,
        },
      })),
    ];

    cyRef.current = cytoscape({
      container: containerRef.current,
      elements: elements,
      style: [
        {
          selector: "node",
          style: {
            shape: "roundrectangle",
            width: "label",
            "min-width": "80px", // ensure a minimum width
            height: "label",
            "min-height": "40px", // ensure a minimum height
            padding: "10px",
            "text-wrap": "wrap",
            "text-max-width": "150px",
            "text-valign": "center",
            "text-halign": "center",
            color: "#fff",
            "font-size": "10px",
          },
        },
        {
          selector: 'node[type="Company"]',
          style: {
            "background-color": "#0074D9",
          },
        },
        {
          selector: 'node[type="FinancialStatement"]',
          style: {
            "background-color": "#FF4136",
          },
        },
        {
          selector: 'node[type="FinancialItem"]',
          style: {
            "background-color": "#2ECC40",
          },
        },
        {
          selector: 'node[type="Period"]',
          style: {
            "background-color": "#FF851B",
          },
        },
        {
          selector: "edge",
          style: {
            width: 2,
            "line-color": "#aaa",
            "target-arrow-color": "#aaa",
            "target-arrow-shape": "triangle",
            "curve-style": "bezier",
            label: "data(label)",
            "font-size": "8px",
            "text-rotation": "autorotate",
          },
        },
      ],
      layout: {
        name: "cose",
        padding: 30,
      },
    });

    return () => {
      if (cyRef.current) {
        cyRef.current.destroy();
      }
    };
  }, [graphData]);

  return (
    <div className="graph-wrapper">
      <div className="graph-visualization-container" ref={containerRef} />
      <div className="legend">
        <h4>Legend</h4>
        <div><strong>Nodes</strong></div>
        <ul>
          <li>
            <span className="legend-color" style={{ backgroundColor: "#0074D9" }}></span>
            Company
          </li>
          <li>
            <span className="legend-color" style={{ backgroundColor: "#FF4136" }}></span>
            Financial Statement
          </li>
          <li>
            <span className="legend-color" style={{ backgroundColor: "#2ECC40" }}></span>
            Financial Item
          </li>
          <li>
            <span className="legend-color" style={{ backgroundColor: "#FF851B" }}></span>
            Period
          </li>
        </ul>
        <div><strong>Edges</strong></div>
        <ul>
          <li>
            <span className="legend-edge"></span>
            HAS_STATEMENT
          </li>
          <li>
            <span className="legend-edge"></span>
            HAS_ITEM
          </li>
          <li>
            <span className="legend-edge"></span>
            HAS_VALUE
          </li>
          <li>
            <span className="legend-edge"></span>
            BREAKDOWN
          </li>
          <li>
            <span className="legend-edge"></span>
            EQUATION
          </li>
        </ul>
      </div>
    </div>
  );
};

export default GraphVisualization;
