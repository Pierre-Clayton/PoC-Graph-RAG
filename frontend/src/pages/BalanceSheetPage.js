// frontend/src/pages/BalanceSheetPage.js
import React, { useState } from "react";
import axios from "axios";

const BalanceSheetPage = () => {
  const [balanceData, setBalanceData] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);

  const backendBaseUrl = "http://localhost:8000";

  const fetchBalanceSheetData = async () => {
    try {
      const res = await axios.get(`${backendBaseUrl}/balance-sheet-data`);
      setBalanceData(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const uploadCSV = async () => {
    if (!selectedFile) {
      alert("Please select a CSV file first.");
      return;
    }
    const formData = new FormData();
    formData.append("file", selectedFile);
    try {
      const res = await axios.post(`${backendBaseUrl}/upload-balance-sheet`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setBalanceData(res.data);
    } catch (err) {
      console.error(err);
      alert("Error uploading the CSV file.");
    }
  };

  return (
    <div>
      <h1>Detailed Balance Sheet Data</h1>
      <div style={{ marginBottom: "20px" }}>
        <button onClick={fetchBalanceSheetData}>
          Generate Default Balance Sheet
        </button>
      </div>
      <div style={{ marginBottom: "20px" }}>
        <h3>Or Upload Your Own CSV File</h3>
        <input type="file" accept=".csv" onChange={handleFileChange} />
        <button onClick={uploadCSV} style={{ marginLeft: "10px" }}>
          Upload CSV
        </button>
      </div>
      {balanceData && (
        <div>
          <h3>Balance Sheet Data</h3>
          <table style={{ borderCollapse: "collapse", width: "100%" }}>
            <thead>
              <tr>
                {balanceData.columns.map((col, index) => (
                  <th
                    key={index}
                    style={{
                      border: "1px solid #ddd",
                      padding: "8px",
                      backgroundColor: "#f2f2f2",
                    }}
                  >
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
