"""Document loaders by file extension.

Registry maps extensions to loader classes. Add new loaders here.
"""
from .pdf import PdfLoader
from .docx import DocxLoader
from .txt import TxtLoader
from .md import MarkdownLoader

_LOADER_REGISTRY = {
    ".pdf": PdfLoader,
    ".docx": DocxLoader,
    ".txt": TxtLoader,
    ".md": MarkdownLoader,
    ".markdown": MarkdownLoader,
}


def get_loader(extension: str):
    """Return the loader class registered for *extension* (e.g. ``.pdf``)."""
    if extension not in _LOADER_REGISTRY:
        raise ValueError(f"Unsupported file extension: {extension}")
    return _LOADER_REGISTRY[extension]
