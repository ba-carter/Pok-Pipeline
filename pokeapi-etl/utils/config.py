import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Database
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "pokemon")

    # API
    POKEAPI_BASE_URL = os.getenv("POKEAPI_BASE_URL", "https://pokeapi.co/api/v2/")
    REQUEST_DELAY = float(os.getenv("REQUEST_DELAY", 0.1))
    API_RETRIES = int(os.getenv("API_RETRIES", 3))
    API_BACKOFF_FACTOR = float(os.getenv("API_BACKOFF_FACTOR", 0.3))

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "pokeapi_etl.log")
