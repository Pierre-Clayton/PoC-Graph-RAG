import React, { useState } from "react";
import axios from "axios";
import "./BalanceSheetPage.css";

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
      const res = await axios.post(
        `${backendBaseUrl}/upload-balance-sheet`,
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );
      setBalanceData(res.data);
    } catch (err) {
      console.error(err);
      alert("Error uploading the CSV file.");
    }
  };

  return (
    <div className="balance-sheet-container">
      <h1>Balance Sheet Analysis</h1>
      <div className="balance-sheet-controls">
        <button onClick={fetchBalanceSheetData} className="primary-button">
          Generate Default Balance Sheet
        </button>
        <div className="upload-section">
          <h3>Or Upload Your CSV File</h3>
          <input type="file" accept=".csv" onChange={handleFileChange} />
          <button onClick={uploadCSV} className="secondary-button">
            Upload CSV
          </button>
        </div>
      </div>
      {balanceData && (
        <div className="data-table">
          <h3>Balance Sheet Data</h3>
          <table>
            <thead>
              <tr>
                {balanceData.columns.map((col, index) => (
                  <th key={index}>{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {balanceData.data.map((row, rowIndex) => (
                <tr key={rowIndex}>
                  {balanceData.columns.map((col, colIndex) => (
                    <td key={colIndex}>{row[col]}</td>
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
