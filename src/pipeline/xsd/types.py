from dataclasses import dataclass
from typing import Optional


@dataclass
class XSDElement:
    name: str
    type: str
    required: bool
    description: Optional[str] = None
    restrictions: Optional[list[str]] = None

@dataclass
class XSDContext:
    schema_name: str
    target_namespace: Optional[str]
    elements: list[XSDElement]
