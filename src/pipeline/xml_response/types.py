from dataclasses import dataclass
from typing import Optional


@dataclass
class XMLNode:
    tag: str
    value: str
    source: Optional[str]

@dataclass
class XMLParseResult:
    nodes: list[XMLNode]
    raw_xml: str