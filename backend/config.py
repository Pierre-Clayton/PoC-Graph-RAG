import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
import matplotlib

# Load environment variables
load_dotenv()

# Configure matplotlib to use the "Agg" backend
matplotlib.use("Agg")

# Neo4j Configuration
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "azertyuiop")
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD), database="trash")

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
