import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
COHERE_MODEL = "command-r-plus-08-2024"
COHERE_EMBEDDING_MODEL = "embed-english-v3.0"

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

DATA_DIR = BASE_DIR / "data"
RAG_DATA_FILE = DATA_DIR / "rag.txt"
CITIES_DATA_FILE = DATA_DIR / "cities.json"
RAG_DB_DIR = BASE_DIR / "rag_db"

SUPPORTED_CITIES = [
    "Paris", "Rome", "Barcelona", "Madrid", "Amsterdam",
    "Berlin", "Milan", "Lisbon", "London", "Vienna"
]

CITY_COORDINATES = {
    "Paris": {"lat": 48.8566, "lon": 2.3522, "country": "France"},
    "Rome": {"lat": 41.9028, "lon": 12.4964, "country": "Italy"},
    "Barcelona": {"lat": 41.3851, "lon": 2.1734, "country": "Spain"},
    "Madrid": {"lat": 40.4168, "lon": -3.7038, "country": "Spain"},
    "Amsterdam": {"lat": 52.3676, "lon": 4.9041, "country": "Netherlands"},
    "Berlin": {"lat": 52.5200, "lon": 13.4050, "country": "Germany"},
    "Milan": {"lat": 45.4642, "lon": 9.1900, "country": "Italy"},
    "Lisbon": {"lat": 38.7223, "lon": -9.1393, "country": "Portugal"},
    "London": {"lat": 51.5074, "lon": -0.1278, "country": "UK"},
    "Vienna": {"lat": 48.2082, "lon": 16.3738, "country": "Austria"}
}

