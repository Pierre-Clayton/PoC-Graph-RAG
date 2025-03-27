import React, { useState } from "react";
import axios from "axios";

const BalanceSheetPage = () => {
  const [prompt, setPrompt] = useState("Enter the prompt to generate the balance sheet...");
  const [balanceData, setBalanceData] = useState(null);

  const backendBaseUrl = "http://localhost:8000";

  const fetchBalanceSheetData = async () => {
    try {
      const res = await axios.get(`${backendBaseUrl}/balance-sheet-data`);
      setBalanceData(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <h1>Generate Balance Sheet Data</h1>
      <div style={{ marginBottom: "20px" }}>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          rows="4"
          style={{ width: "100%", padding: "10px" }}
        />
        <button onClick={fetchBalanceSheetData} style={{ marginTop: "10px" }}>
          Generate Balance Sheet
        </button>
      </div>
      {balanceData && (
        <div>
          <h3>Balance Sheet Data</h3>
          <table style={{ borderCollapse: "collapse", width: "100%" }}>
            <thead>
              <tr>
                {balanceData.columns.map((col, index) => (
                  <th key={index} style={{ border: "1px solid #ddd", padding: "8px", backgroundColor: "#f2f2f2" }}>
                    {col}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {balanceData.data.map((row, rowIndex) => (
                <tr key={rowIndex}>
                  {balanceData.columns.map((col, colIndex) => (
                    <td key={colIndex} style={{ border: "1px solid #ddd", padding: "8px" }}>
                      {row[col]}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default BalanceSheetPage;
