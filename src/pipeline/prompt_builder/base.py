from typing import Protocol, List
from pipeline.types import ParsedBlock


class PromptBuilder(Protocol):
    def build(self, blocks: List[ParsedBlock]) -> str:
        ...
