"""Abstract base class for document loaders."""
from abc import ABC, abstractmethod
from typing import Optional


class BaseLoader(ABC):
    """Interface that all file-type loaders must implement."""

    @abstractmethod
    def load(self, path: Optional[str] = None, raw_text: Optional[str] = None) -> str:
        """Extract text content from a file (by path) or return raw_text."""
        ...

    @abstractmethod
    def supported_extensions(self) -> list[str]:
        """Return the file extensions this loader handles (e.g. ``['.pdf']``)."""
        ...