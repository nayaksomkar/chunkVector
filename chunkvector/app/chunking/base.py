"""Abstract base class for text splitters."""
from abc import ABC, abstractmethod
from typing import List


class BaseSplitter(ABC):
    """Interface that all chunking strategies must implement."""

    @abstractmethod
    def split_text(self, text: str) -> List[str]:
        """Split a single string into a list of non-overlapping text chunks."""
        ...