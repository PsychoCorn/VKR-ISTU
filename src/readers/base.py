from typing import Protocol


class DocumentReader(Protocol):
    def read(self, path: str) -> str:
        """
        Reads document content and returns plain text representation.
        """
        ...
