"""Application configuration via environment variables.

Uses pydantic-settings to load from environment variables or an optional .env file.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables or .env file.

    All values can be overridden via environment variables or a .env file.
    """

    # Chunking
    chunk_size: int = 1000
    chunk_overlap: int = 200

    # Embeddings
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Vector store
    chroma_persist_directory: str = "./chroma_db"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # ChromaDB
    chroma_host: str | None = None
    chroma_port: int | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Singleton config — import this in other modules
settings = Settings()