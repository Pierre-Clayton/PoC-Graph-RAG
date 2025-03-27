import React, { useState } from "react";
import axios from "axios";
import Navigation from "./components/Navigation";
import Analysis from "./components/Analysis";
import GraphVisualization from "./components/GraphVisualization";

function App() {
  const [balanceData, setBalanceData] = useState(null);
  const [graphJson, setGraphJson] = useState(null);
  const [classicAnalysis, setClassicAnalysis] = useState("");
  const [graphAnalysis, setGraphAnalysis] = useState("");
  const [graphImage, setGraphImage] = useState(null);

  const backendBaseUrl = "http://localhost:8000";

  const fetchBalanceSheetData = async () => {
    try {
      const res = await axios.get(`${backendBaseUrl}/balance-sheet-data`);
      setBalanceData(res.data.csv);
    } catch (err) {
      console.error(err);
    }
  };

  const generateGraphJson = async () => {
    try {
      const res = await axios.post(`${backendBaseUrl}/generate-graph-json`);
      setGraphJson(JSON.stringify(res.data, null, 2));
    } catch (err) {
      console.error(err);
    }
  };

  const insertGraph = async () => {
    try {
      const res = await axios.post(`${backendBaseUrl}/insert-graph`);
      alert(res.data.status);
    } catch (err) {
      console.error(err);
    }
  };

  const getClassicAnalysis = async () => {
    try {
      const res = await axios.post(`${backendBaseUrl}/classic-analysis`);
      setClassicAnalysis(res.data.classic_analysis);
    } catch (err) {
      console.error(err);
    }
  };

  const getGraphAnalysis = async () => {
    try {
      const res = await axios.post(`${backendBaseUrl}/graph-analysis`);
      setGraphAnalysis(res.data.graph_analysis);
    } catch (err) {
      console.error(err);
    }
  };

  const getGraphVisualization = async () => {
    try {
      // Pour récupérer l'image, on force le type blob.
      const res = await axios.get(`${backendBaseUrl}/visualize-graph`, { responseType: "blob" });
      const imageUrl = URL.createObjectURL(res.data);
      setGraphImage(imageUrl);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="App" style={{ padding: "20px" }}>
      <Navigation />
      <h1>Financial Knowledge Graph App</h1>
      <div>
        <button onClick={fetchBalanceSheetData}>Charger données de bilan</button>
        {balanceData && (
          <pre style={{ backgroundColor: "#f4f4f4", padding: "10px", overflow: "auto" }}>
            {balanceData}
          </pre>
        )}
      </div>
      <div style={{ marginTop: "20px" }}>
        <button onClick={generateGraphJson}>Générer Graph JSON</button>
        {graphJson && (
          <pre style={{ backgroundColor: "#f4f4f4", padding: "10px", overflow: "auto" }}>
            {graphJson}
          </pre>
        )}
      </div>
      <div style={{ marginTop: "20px" }}>
        <button onClick={insertGraph}>Insérer Graph dans Neo4j</button>
      </div>
      <div style={{ marginTop: "20px" }}>
        <button onClick={getClassicAnalysis}>Obtenir Analyse Classique</button>
        {classicAnalysis && <Analysis title="Analyse Classique" analysis={classicAnalysis} />}
      </div>
      <div style={{ marginTop: "20px" }}>
        <button onClick={getGraphAnalysis}>Obtenir Analyse Graph</button>
        {graphAnalysis && <Analysis title="Analyse Graph" analysis={graphAnalysis} />}
      </div>
      <div style={{ marginTop: "20px" }}>
        <button onClick={getGraphVisualization}>Visualiser Graph</button>
        {graphImage && <GraphVisualization imageUrl={graphImage} />}
      </div>
    </div>
  );
}

export default App;
