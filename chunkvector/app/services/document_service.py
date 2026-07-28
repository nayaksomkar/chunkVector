"""Document ingestion orchestration service.

Loads raw text from files (PDF, DOCX, TXT, MD), runs the cleaning pipeline,
splits text into chunks via the requested splitter, generates embeddings,
and persists everything to ChromaDB with timing instrumentation.
"""
import logging
import time
import uuid
from datetime import datetime

from chunkvector.app.config import settings
from chunkvector.app.cleaning import clean_text
from chunkvector.app.chunking.splitter import (
    RecursiveCharacterSplitter,
    CharacterSplitter,
    TokenSplitter,
)
from chunkvector.app.embeddings.manager import EmbeddingManager
from chunkvector.app.vectordb.store import ChromaStore
from chunkvector.app.schemas.document import DocumentProcessRequest, DocumentMetadata


logger = logging.getLogger(__name__)

# Maps user-facing splitter names to implementation classes
SPLITTER_MAP = {
    "recursive_character": RecursiveCharacterSplitter,
    "character": CharacterSplitter,
    "token": TokenSplitter,
}


class DocumentService:
    """Orchestrates the document processing pipeline end-to-end."""

    def __init__(self):
        self.embedding_manager = EmbeddingManager()
        self.chroma_store = ChromaStore()

    def _get_splitter(self, splitter_type: str):
        """Look up and instantiate a text splitter by type name."""
        splitter_cls = SPLITTER_MAP.get(splitter_type)
        if splitter_cls is None:
            raise ValueError(f"Unknown splitter type: {splitter_type}")
        return splitter_cls(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )

    def process_document(
        self,
        request: DocumentProcessRequest,
        splitter_type: str = "recursive_character",
    ) -> dict:
        """Run the full pipeline: extract → clean → chunk → embed → store.

        Returns a summary dict with chunk count, splitter used, and per-stage
        timing (seconds).
        """
        # ---- Stage 1: Extract raw text -----------------------------------
        start_extraction = time.time()

        if request.document_path:
            ext = "." + request.document_path.rsplit(".", 1)[-1].lower()
            from chunkvector.app.loaders import get_loader
            loader = get_loader(ext)
            raw_text = loader.load(path=request.document_path)
        elif request.raw_text:
            raw_text = request.raw_text
        else:
            raise ValueError("Either document_path or raw_text must be provided")

        extraction_time = time.time() - start_extraction

        # ---- Stage 2: Clean text -----------------------------------------
        cleaned = clean_text(raw_text)

        # ---- Stage 3: Chunk ----------------------------------------------
        start_chunking = time.time()
        splitter = self._get_splitter(splitter_type)
        chunks = splitter.split_text(cleaned)
        chunking_time = time.time() - start_chunking

        # Build per-chunk metadata
        chunk_ids = [str(uuid.uuid4()) for _ in chunks]
        metadata_list = [
            DocumentMetadata(
                document_id=request.source,
                filename=request.document_path or "raw_text",
                page=None,
                chunk_id=chunk_id,
                chunk_number=i,
                source=request.source,
                timestamp=datetime.utcnow(),
            ).model_dump()
            for i, chunk_id in enumerate(chunk_ids)
        ]

        # ---- Stage 4: Embed ----------------------------------------------
        start_embedding = time.time()
        embeddings = self.embedding_manager.embed(chunks)
        embedding_time = time.time() - start_embedding

        # ---- Stage 5: Store in vector DB ---------------------------------
        start_insertion = time.time()
        self.chroma_store.add(
            ids=chunk_ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadata_list,
        )
        insertion_time = time.time() - start_insertion

        logger.info(
            "Processing complete: extraction=%.3fs, chunks=%d, embedding=%.3fs, insertion=%.3fs",
            extraction_time,
            len(chunks),
            embedding_time,
            insertion_time,
        )

        return {
            "document_id": request.source,
            "chunks_count": len(chunks),
            "splitter_type": splitter_type,
            "timing": {
                "extraction_seconds": round(extraction_time, 4),
                "chunking_seconds": round(chunking_time, 4),
                "embedding_seconds": round(embedding_time, 4),
                "chromadb_insertion_seconds": round(insertion_time, 4),
            },
        }