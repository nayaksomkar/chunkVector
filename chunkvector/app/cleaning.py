"""Text cleaning utilities for normalizing document content before chunking.

Applies a pipeline of Unicode normalization, whitespace collapse, paragraph
preservation, and empty-line removal.
"""
from typing import Optional
import unicodedata


def normalize_unicode(text: str) -> str:
    """Normalize Unicode to NFKC form (compatibility composition)."""
    return unicodedata.normalize("NFKC", text)


def normalize_whitespace(text: str) -> str:
    """Collapse multiple spaces/tabs on each line into a single space."""
    lines = text.split("\n")
    normalized: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped:
            normalized.append(" ".join(stripped.split()))
        else:
            normalized.append("")
    return "\n".join(normalized)


def remove_empty_lines(text: str) -> str:
    """Drop lines that are empty or contain only whitespace."""
    lines = text.split("\n")
    cleaned = [line for line in lines if line.strip()]
    return "\n".join(cleaned)


def preserve_paragraphs(text: str) -> str:
    """Join consecutive non-empty lines into paragraphs separated by blank lines."""
    lines = text.split("\n")
    paragraphs: list[str] = []
    current: list[str] = []
    for line in lines:
        if line.strip():
            current.append(line.strip())
        else:
            if current:
                paragraphs.append(" ".join(current))
                current = []
    if current:
        paragraphs.append(" ".join(current))
    return "\n\n".join(paragraphs)


def clean_text(text: str) -> str:
    """Run the full cleaning pipeline on raw extracted text.

    Pipeline order: Unicode NFKC → whitespace collapse → paragraph join
    → empty-line removal → final strip.
    """
    text = normalize_unicode(text)
    text = normalize_whitespace(text)
    text = preserve_paragraphs(text)
    text = remove_empty_lines(text)
    return text.strip()


def extract_text_from_loader(
    loader_class, path: Optional[str] = None, raw_text: Optional[str] = None
) -> str:
    """Convenience: instantiate a loader class and call its load method."""
    loader = loader_class()
    return loader.load(path=path, raw_text=raw_text)