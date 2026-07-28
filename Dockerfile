FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY chunkvector/ ./chunkvector/

EXPOSE 8000

ENV CHUNK_SIZE=1000
ENV CHUNK_OVERLAP=200
ENV EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
ENV CHROMA_PERSIST_DIR=/app/chroma_db
ENV HOST=0.0.0.0
ENV PORT=8000

CMD ["uvicorn", "chunkvector.app.main:app", "--host", "0.0.0.0", "--port", "8000"]