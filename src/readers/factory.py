from pathlib import Path
from typing import Dict, Type

from .base import DocumentReader
from .docx_reader import DocxReader


_READERS: Dict[str, Type[DocumentReader]] = {
    ".docx": DocxReader,
}


def get_reader(path: str) -> DocumentReader:
    ext = Path(path).suffix.lower()

    if ext not in _READERS:
        raise ValueError(f"Unsupported document type: {ext}")

    return _READERS[ext]()
