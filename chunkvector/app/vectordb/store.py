"""ChromaDB vector-store wrapper.

Handles collection lifecycle (get-or-create, delete, list) and provides
strongly-typed add/query methods backed by cosine similarity.
"""
import logging
from typing import List

import chromadb
from chunkvector.app.config import settings


logger = logging.getLogger(__name__)


class ChromaStore:
    """Thin wrapper around a persistent or remote ChromaDB collection."""

    def __init__(self, collection_name: str = "documents", persist_directory: str | None = None):
        persist_directory = persist_directory or settings.chroma_persist_directory
        if settings.chroma_host:
            self.client = chromadb.HttpClient(host=settings.chroma_host, port=settings.chroma_port or 8000)
        else:
            self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection_name = collection_name
        self._collection = self._get_or_create_collection()

    def _get_or_create_collection(self):
        """Fetch existing collection or create a new one with cosine distance."""
        try:
            collection = self.client.get_collection(name=self.collection_name)
        except Exception:
            collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"},
            )
        return collection

    def add(
        self,
        ids: List[str],
        documents: List[str],
        embeddings: List[List[float]],
        metadatas: List[dict],
    ):
        """Insert records into the collection."""
        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )
        logger.info("Inserted %d records into ChromaDB collection '%s'", len(ids), self.collection_name)

    def query(self, query_embeddings: List[List[float]], n_results: int = 5):
        """Search the collection by embedding vector similarity."""
        results = self.collection.query(
            query_embeddings=query_embeddings,
            n_results=n_results,
        )
        return results

    def delete_collection(self, collection_name: str):
        """Delete a collection by name; no-op if it doesn't exist."""
        try:
            self.client.delete_collection(name=collection_name)
            logger.info("Deleted collection '%s'", collection_name)
        except Exception:
            pass

    def list_collections(self) -> list[str]:
        """Return names of all existing collections."""
        return [c.name for c in self.client.list_collections()]

    def reset(self):
        """Wipe all collections (use with care)."""
        self.client.reset()