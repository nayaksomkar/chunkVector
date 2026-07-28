"""LangChain-based text splitter implementations.

Wraps three common LangChain splitters behind the ``BaseSplitter`` interface
so callers can swap strategies without depending on LangChain internals.
"""
from typing import List
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    TokenTextSplitter,
)
from .base import BaseSplitter


class RecursiveCharacterSplitter(BaseSplitter):
    """Splits text recursively on characters (default: ``["\\n\\n", "\\n", " ", ""]``).

    Generally the best default for prose documents.
    """

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def split_text(self, text: str) -> List[str]:
        return self._splitter.split_text(text)


class CharacterSplitter(BaseSplitter):
    """Splits on a fixed separator character (default: newline)."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200, separator: str = "\n"):
        self._splitter = CharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separator=separator,
        )

    def split_text(self, text: str) -> List[str]:
        return self._splitter.split_text(text)


class TokenSplitter(BaseSplitter):
    """Splits text on token boundaries using a HuggingFace/tiktoken tokenizer."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200, encoding_model: str = "gpt2"):
        self._splitter = TokenTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            encoding_model=encoding_model,
        )

    def split_text(self, text: str) -> List[str]:
        return self._splitter.split_text(text)