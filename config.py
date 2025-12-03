"""
Configuration file for Travel Guide application.
Centralized configuration for API keys, models, and paths.
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# API Configuration
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
COHERE_MODEL = "command-r-plus-08-2024"
COHERE_EMBEDDING_MODEL = "embed-english-v3.0"

# Data paths
DATA_DIR = BASE_DIR / "data"
RAG_DATA_FILE = DATA_DIR / "rag.txt"
RAG_DB_DIR = BASE_DIR / "rag_db"

