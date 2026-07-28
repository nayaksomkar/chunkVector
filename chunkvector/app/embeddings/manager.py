"""Embedding manager wrapping SentenceTransformers.

Loads a model once and provides batched ``embed`` and single ``embed_query``
methods with L2-normalised outputs (compatible with cosine similarity).
"""
import logging
from typing import List
from sentence_transformers import SentenceTransformer
from chunkvector.app.config import settings


logger = logging.getLogger(__name__)


class EmbeddingManager:
    """Manages a SentenceTransformer model for document & query embeddings."""

    def __init__(self, model_name: str | None = None):
        model_name = model_name or settings.embedding_model_name
        logger.info("Loading embedding model: %s", model_name)
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name

    def embed(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of texts into a list of normalised float vectors."""
        logger.info("Generating embeddings for %d texts", len(texts))
        embeddings = self.model.encode(texts, normalize_embeddings=True)
        return embeddings.tolist()

    def embed_query(self, query: str) -> List[float]:
        """Embed a single query string into a normalised float vector."""
        embedding = self.model.encode(query, normalize_embeddings=True)
        return embedding.tolist()