import React from "react";
import "./HomePage.css";

const HomePage = () => {
  return (
    <div className="home-container">
      <header className="home-header">
        <h1>Welcome to the Financial Knowledge Graph App</h1>
        <p>
          Explore advanced financial data analysis using our innovative Graph RAG method.
        </p>
      </header>

      <section className="home-section">
        <h2>Graph RAG Methodology</h2>
        <p>
          Graph RAG (Graph-based Retrieval Augmented Generation) is a cutting-edge approach that integrates graph databases with retrieval augmented generation. By leveraging structured relationships within financial data, this method provides a deeper, context-aware analysis.
        </p>
        <ul>
          <li>
            <strong>Structured Data Representation:</strong> Models financial data as nodes and edges.
          </li>
          <li>
            <strong>Enhanced Context Retrieval:</strong> Extracts relevant, context-linked data points.
          </li>
          <li>
            <strong>Dynamic Analysis:</strong> Offers interactive graph visualizations and in-depth insights.
          </li>
          <li>
            <strong>Optimized Summarization:</strong> Uses AI to generate detailed analyses based on both direct and indirect relationships.
          </li>
        </ul>
      </section>

      <section className="home-section">
        <h2>Comparison with Classic RAG</h2>
        <div className="comparison-container">
          <div className="comparison-card">
            <h3>Graph RAG</h3>
            <p>
              Utilizes graph structures to capture relational insights and deliver interactive visual analysis.
            </p>
            <ul>
              <li>Structured relationships</li>
              <li>Context-aware retrieval</li>
              <li>Interactive visualizations</li>
              <li>Enhanced financial insights</li>
            </ul>
          </div>
          <div className="comparison-card">
            <h3>Classic RAG</h3>
            <p>
              Relies primarily on text-based retrieval with limited ability to capture complex relationships.
            </p>
            <ul>
              <li>Unstructured data analysis</li>
              <li>Standard summarization techniques</li>
              <li>Less interactive</li>
              <li>Limited context extraction</li>
            </ul>
          </div>
        </div>
      </section>

      <section className="home-section">
        <h2>How It Works</h2>
        <p>
          Our application uses a FastAPI backend integrated with a Neo4j graph database and OpenAI’s language models. The balance sheet data from BNP Paribas is transformed into a dynamic knowledge graph, which is then visualized interactively. This end-to-end process ensures that users receive not only raw data but also actionable insights through both classic and graph-based analyses.
        </p>
      </section>

      <footer className="home-footer">
        <p>
          Use the navigation links above to generate balance sheets, explore the interactive graph, or chat with our analysis bot.
        </p>
      </footer>
    </div>
  );
};

export default HomePage;
