import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
COHERE_MODEL = "command-r-plus-08-2024"
COHERE_EMBEDDING_MODEL = "embed-english-v3.0"

DATA_DIR = BASE_DIR / "data"
RAG_DATA_FILE = DATA_DIR / "rag.txt"
RAG_DB_DIR = BASE_DIR / "rag_db"

