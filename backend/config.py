import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
import matplotlib

# Charger les variables d'environnement
load_dotenv()

# Configurer matplotlib pour utiliser le backend "Agg"
matplotlib.use("Agg")

# Configuration de Neo4j
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "azertyuiop")
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD), database="trash")

# Clé API OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
