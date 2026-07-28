"""Markdown file loader."""
from typing import Optional
from .base import BaseLoader


class MarkdownLoader(BaseLoader):
    """Read a Markdown file (.md / .markdown) and return its full contents."""

    def load(self, path: Optional[str] = None, raw_text: Optional[str] = None) -> str:
        if raw_text is not None:
            return raw_text
        if path is None:
            raise ValueError("A file path is required for Markdown loading")
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def supported_extensions(self) -> list[str]:
        return [".md", ".markdown"]