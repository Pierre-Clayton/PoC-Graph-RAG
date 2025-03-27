// frontend/src/pages/BalanceSheetPage.js
import React, { useState } from "react";
import axios from "axios";

const BalanceSheetPage = () => {
  const [prompt, setPrompt] = useState("Entrez le prompt pour générer le bilan...");
  const [balanceData, setBalanceData] = useState("");

  const backendBaseUrl = "http://localhost:8000";

  const fetchBalanceSheetData = async () => {
    try {
      const res = await axios.get(`${backendBaseUrl}/balance-sheet-data`);
      setBalanceData(res.data.csv);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <h1>Générer les données de Bilan</h1>
      <div style={{ marginBottom: "20px" }}>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          rows="4"
          style={{ width: "100%", padding: "10px" }}
        />
        <button onClick={fetchBalanceSheetData} style={{ marginTop: "10px" }}>
          Générer Bilan
        </button>
      </div>
      {balanceData && (
        <div>
          <h3>Données de Bilan</h3>
          <pre style={{ backgroundColor: "#f4f4f4", padding: "10px", overflow: "auto" }}>
            {balanceData}
          </pre>
        </div>
      )}
    </div>
  );
};

export default BalanceSheetPage;
