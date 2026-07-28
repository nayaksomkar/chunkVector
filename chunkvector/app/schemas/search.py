"""Pydantic models for search requests and results."""
from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    """Request body for the semantic search endpoint."""

    query: str = Field(..., description="Search query text")
    top_k: int = Field(default=5, ge=1, le=100, description="Number of results to return")


class SearchResult(BaseModel):
    """A single ranked result from a similarity search."""

    chunk: str = Field(..., description="The text content of the matching chunk")
    metadata: dict = Field(..., description="Metadata associated with the chunk")
    score: float = Field(..., description="Similarity score of the result")