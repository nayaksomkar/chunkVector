"""Text chunking strategies.

All splitters implement ``BaseSplitter.split_text(text: str) -> list[str]``.
"""
from .splitter import (
    RecursiveCharacterSplitter,
    CharacterSplitter,
    TokenSplitter,
)

__all__ = [
    "RecursiveCharacterSplitter",
    "CharacterSplitter",
    "TokenSplitter",
]
