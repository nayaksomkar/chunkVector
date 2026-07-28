"""PDF text loader using PyPDF2."""
from typing import Optional
from PyPDF2 import PdfReader
from .base import BaseLoader


class PdfLoader(BaseLoader):
    """Extract text from each page of a PDF, joined by newlines."""

    def load(self, path: Optional[str] = None, raw_text: Optional[str] = None) -> str:
        if raw_text is not None:
            return raw_text
        if path is None:
            raise ValueError("A file path is required for PDF loading")
        reader = PdfReader(path)
        text_parts: list[str] = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
        return "\n".join(text_parts)

    def supported_extensions(self) -> list[str]:
        return [".pdf"]