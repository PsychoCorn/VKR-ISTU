from dataclasses import dataclass


@dataclass
class XSDValidationError:
    message: str
    line: int | None
    column: int | None

@dataclass
class XSDValidationResult:
    is_valid: bool
    errors: list[XSDValidationError]