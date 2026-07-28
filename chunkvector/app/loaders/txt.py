"""Plain-text file loader."""
from typing import Optional
from .base import BaseLoader


class TxtLoader(BaseLoader):
    """Read a UTF-8 text file and return its full contents."""

    def load(self, path: Optional[str] = None, raw_text: Optional[str] = None) -> str:
        if raw_text is not None:
            return raw_text
        if path is None:
            raise ValueError("A file path is required for TXT loading")
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def supported_extensions(self) -> list[str]:
        return [".txt"]