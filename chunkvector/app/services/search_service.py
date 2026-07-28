"""Vector search service.

Embeds a query string and performs similarity search against the ChromaDB
collection, returning ranked results with scores and metadata.
"""
import logging
from typing import List

from chunkvector.app.embeddings.manager import EmbeddingManager
from chunkvector.app.vectordb.store import ChromaStore
from chunkvector.app.schemas.search import SearchResult


logger = logging.getLogger(__name__)


class SearchService:
    """Semantic search over previously ingested and embedded documents."""

    def __init__(self):
        self.embedding_manager = EmbeddingManager()
        self.chroma_store = ChromaStore()

    def search(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """Embed the query and return the top-k most similar chunks.

        Results include the chunk text, metadata, and similarity distance score.
        """
        query_embedding = self.embedding_manager.embed_query(query)
        results = self.chroma_store.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        search_results: list[SearchResult] = []
        if results and results.get("documents"):
            for i in range(len(results["documents"][0])):
                search_results.append(
                    SearchResult(
                        chunk=results["documents"][0][i],
                        metadata=results["metadatas"][0][i] if results.get("metadatas") else {},
                        score=results["distances"][0][i] if results.get("distances") else 0.0,
                    )
                )

        logger.info("Search for query '%s' returned %d results", query, len(search_results))
        return search_results