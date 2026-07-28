# ChunkVector

> AI backend microservice for document ingestion, chunking, embedding generation, and vector similarity search.

**Stack:** FastAPI · LangChain · ChromaDB · SentenceTransformers

---

## Features

- **Multi-format ingestion** — PDF, DOCX, TXT, Markdown
- **Text cleaning pipeline** — Unicode NFKC normalisation, whitespace collapse, paragraph preservation
- **Three chunking strategies** — `recursive_character`, `character`, `token` (via LangChain)
- **Embeddings** — SentenceTransformers (`all-MiniLM-L6-v2`), configurable model
- **Vector search** — Cosine similarity via ChromaDB with ranked results + metadata
- **Collection management** — List / delete vector collections via REST
- **Instrumented pipeline** — Per-stage timing logged (extraction, chunking, embedding, insertion)
- **Dockerised** — Ready-to-deploy container

---

## Quick start

### Prerequisites

- Python ≥ 3.11
- `pip`

### Local

```bash
# 1. Clone and enter the repo
git clone https://github.com/<you>/chunkvector && cd chunkvector

# 2. (Optional) Create a virtual environment
python -m venv .venv && source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the server
uvicorn chunkvector.app.main:app --host 0.0.0.0 --port 8000
```

The API is now live at `http://localhost:8000`.  
OpenAPI docs: `http://localhost:8000/docs`

### Docker

```bash
docker build -t chunkvector .
docker run -p 8000:8000 chunkvector
```

---

## API Reference

### `POST /api/v1/ingest`
Ingest a document using the default `recursive_character` splitter.

```bash
curl -X POST http://localhost:8000/api/v1/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "document_path": "/data/report.pdf",
    "source": "quarterly_report"
  }'
```

**Response**
```json
{
  "document_id": "quarterly_report",
  "chunks_count": 12,
  "splitter_type": "recursive_character",
  "timing": {
    "extraction_seconds": 0.234,
    "chunking_seconds": 0.012,
    "embedding_seconds": 0.876,
    "chromadb_insertion_seconds": 0.045
  }
}
```

### `POST /api/v1/ingest/{splitter_type}`
Ingest with an explicit splitter type.

```bash
curl -X POST http://localhost:8000/api/v1/ingest/token \
  -H "Content-Type: application/json" \
  -d '{
    "document_path": "/data/codebase.py",
    "source": "source_code"
  }'
```

**Splitter types:** `recursive_character`, `character`, `token`

### `POST /api/v1/search`
Semantic search over ingested chunks.

```bash
curl -X POST http://localhost:8000/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the project about?",
    "top_k": 5
  }'
```

**Response**
```json
[
  {
    "chunk": "The project is an AI-powered document analysis platform...",
    "metadata": {
      "document_id": "quarterly_report",
      "filename": "/data/report.pdf",
      "chunk_number": 3,
      "source": "quarterly_report"
    },
    "score": 0.8472
  }
]
```

### `GET /api/v1/collections`
List all ChromaDB collections.

```bash
curl http://localhost:8000/api/v1/collections
```

### `DELETE /api/v1/collections/{collection_name}`
Delete a specific collection and its data.

```bash
curl -X DELETE http://localhost:8000/api/v1/collections/documents
```

### `GET /health`
Liveness probe.

```bash
curl http://localhost:8000/health
# → {"status": "ok"}
```

---

## Configuration

All settings can be overridden via environment variables or a `.env` file.

| Variable | Default | Description |
|---|---|---|
| `CHUNK_SIZE` | `1000` | Target chunk size (characters or tokens) |
| `CHUNK_OVERLAP` | `200` | Overlap between consecutive chunks |
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | HuggingFace embedding model name |
| `CHROMA_PERSIST_DIR` | `./chroma_db` | Directory for ChromaDB persistence |
| `HOST` | `0.0.0.0` | Server bind address |
| `PORT` | `8000` | Server port |

Example `.env` file:

```ini
CHUNK_SIZE=500
CHUNK_OVERLAP=50
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
CHROMA_PERSIST_DIR=/data/chroma
```

---

## Project Structure

```
chunkvector/
├── chunkvector/
│   └── app/
│       ├── __init__.py
│       ├── main.py                  # FastAPI app entry point
│       ├── config.py                # Environment-based settings
│       ├── cleaning.py              # Text normalisation utilities
│       ├── api/
│       │   ├── __init__.py
│       │   └── routes.py            # REST endpoint definitions
│       ├── chunking/
│       │   ├── __init__.py
│       │   ├── base.py              # Abstract splitter interface
│       │   └── splitter.py          # LangChain splitter wrappers
│       ├── embeddings/
│       │   ├── __init__.py
│       │   └── manager.py           # SentenceTransformer wrapper
│       ├── loaders/
│       │   ├── __init__.py          # Loader registry
│       │   ├── base.py              # Abstract loader interface
│       │   ├── pdf.py
│       │   ├── docx.py
│       │   ├── txt.py
│       │   └── md.py
│       ├── schemas/
│       │   ├── __init__.py
│       │   ├── document.py          # Pydantic models for ingestion
│       │   └── search.py            # Pydantic models for search
│       ├── services/
│       │   ├── __init__.py
│       │   ├── document_service.py  # Ingestion orchestration
│       │   └── search_service.py    # Search orchestration
│       └── vectordb/
│           ├── __init__.py
│           └── store.py             # ChromaDB wrapper
├── Dockerfile
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## Development

```bash
# Install dev extras
pip install -e ".[dev]"

# Lint
ruff check chunkvector/

# Type-check (install basedpyright or pyright)
basedpyright chunkvector/
```