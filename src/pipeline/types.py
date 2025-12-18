# pipeline/types.py
from dataclasses import dataclass
from typing import Literal


BlockType = Literal["paragraph", "table", "comment"]


@dataclass
class ParsedBlock:
    block_id: str
    type: BlockType
    content: str
    source: str  # e.g. "docx:p3", "docx:table1:row2", "user:comment"
