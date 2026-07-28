"""FastAPI application entry point for ChunkVector.

Exposes the ASGI app instance for uvicorn/gunicorn and mounts all API routers.
"""
from fastapi import FastAPI
from chunkvector.app.api.routes import router, collections_router

# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------
app = FastAPI(
    title="ChunkVector",
    description="AI backend microservice for document ingestion, chunking, embedding, and vector search",
    version="0.1.0",
)

# Mount ingest/search routes and collection management routes under /api/v1
app.include_router(router, prefix="/api/v1")
app.include_router(collections_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    """Simple liveness probe — returns ok when the service is running."""
    return {"status": "ok"}