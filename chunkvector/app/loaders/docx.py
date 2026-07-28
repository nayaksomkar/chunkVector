"""DOCX text loader using python-docx."""
from typing import Optional
from docx import Document
from .base import BaseLoader


class DocxLoader(BaseLoader):
    """Extract text from all paragraphs of a .docx file."""

    def load(self, path: Optional[str] = None, raw_text: Optional[str] = None) -> str:
        if raw_text is not None:
            return raw_text
        if path is None:
            raise ValueError("A file path is required for DOCX loading")
        doc = Document(path)
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n".join(paragraphs)

    def supported_extensions(self) -> list[str]:
        return [".docx"]