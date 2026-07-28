"""Pydantic models for document ingestion requests and chunk metadata."""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class DocumentMetadata(BaseModel):
    """Metadata attached to each chunk stored in the vector database."""

    document_id: str = Field(..., description="Unique identifier for the document")
    filename: str = Field(..., description="Name of the source file")
    page: Optional[int] = Field(None, description="Page number if applicable")
    chunk_id: str = Field(..., description="Unique identifier for the chunk")
    chunk_number: int = Field(..., description="Sequential number of the chunk")
    source: str = Field(..., description="Path or identifier of the source document")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class DocumentProcessRequest(BaseModel):
    """Request body for the document ingestion endpoint."""

    document_path: Optional[str] = Field(None, description="Path to the document file")
    raw_text: Optional[str] = Field(None, description="Raw text content")
    source: Optional[str] = Field("unknown", description="Source identifier for the document")