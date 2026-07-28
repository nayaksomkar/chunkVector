"""FastAPI route handlers for document ingestion, search, and collection management.

Routes are split across two routers:
- ``router``        → ingest & search endpoints
- ``collections_router`` → collection CRUD (list / delete)
"""
import logging
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from chunkvector.app.schemas.document import DocumentProcessRequest
from chunkvector.app.schemas.search import SearchRequest, SearchResult
from chunkvector.app.services.document_service import DocumentService
from chunkvector.app.services.search_service import SearchService
from chunkvector.app.vectordb.store import ChromaStore


logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Lazy-loaded service singletons
# ---------------------------------------------------------------------------
router = APIRouter()

_document_service: Optional[DocumentService] = None
_search_service: Optional[SearchService] = None


def get_document_service() -> DocumentService:
    """Return (and cache) the singleton DocumentService."""
    global _document_service
    if _document_service is None:
        _document_service = DocumentService()
    return _document_service


def get_search_service() -> SearchService:
    """Return (and cache) the singleton SearchService."""
    global _search_service
    if _search_service is None:
        _search_service = SearchService()
    return _search_service


# ---------------------------------------------------------------------------
# Ingest endpoints
# ---------------------------------------------------------------------------


@router.post("/ingest")
async def ingest_document(request: DocumentProcessRequest):
    """Ingest a document using the default recursive-character splitter.

    Body can provide a ``document_path`` or ``raw_text``.
    """
    try:
        service = get_document_service()
        result = service.process_document(
            request=request,
            splitter_type="recursive_character",
        )
        return result
    except Exception as e:
        logger.error("Ingestion failed: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ingest/{splitter_type}")
async def ingest_document_with_splitter(splitter_type: str, request: DocumentProcessRequest):
    """Ingest a document with an explicit splitter type.

    Supported splitter types: ``recursive_character``, ``character``, ``token``.
    """
    try:
        service = get_document_service()
        result = service.process_document(
            request=request,
            splitter_type=splitter_type,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("Ingestion failed: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# Search endpoint
# ---------------------------------------------------------------------------


@router.post("/search", response_model=List[SearchResult])
async def search(request: SearchRequest):
    """Semantic search over ingested document chunks."""
    try:
        service = get_search_service()
        results = service.search(query=request.query, top_k=request.top_k)
        return results
    except Exception as e:
        logger.error("Search failed: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# Collection management endpoints
# ---------------------------------------------------------------------------

collections_router = APIRouter()


@collections_router.get("/collections")
async def list_collections():
    """List all ChromaDB collections."""
    try:
        store = ChromaStore()
        collections = store.list_collections()
        return {"collections": collections}
    except Exception as e:
        logger.error("Failed to list collections: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@collections_router.delete("/collections/{collection_name}")
async def delete_collection(collection_name: str):
    """Delete a named ChromaDB collection and all its data."""
    try:
        store = ChromaStore()
        store.delete_collection(collection_name)
        return {"message": f"Collection '{collection_name}' deleted"}
    except Exception as e:
        logger.error("Failed to delete collection '%s': %s", collection_name, str(e))
        raise HTTPException(status_code=500, detail=str(e))