from lxml import etree
from pathlib import Path

from .validation_types import (
    XSDValidationResult,
    XSDValidationError,
)

class XSDValidator:
    def __init__(self, xsd_path: str):
        self.xsd_path = Path(xsd_path)

        if not self.xsd_path.exists():
            raise FileNotFoundError(f"XSD file not found: {xsd_path}")

        self._schema = self._load_schema()

    def _load_schema(self) -> etree.XMLSchema:
        try:
            xsd_tree = etree.parse(str(self.xsd_path))
            return etree.XMLSchema(xsd_tree)
        except etree.XMLSchemaParseError as e:
            raise ValueError(f"Invalid XSD schema: {e}")
        
    def validate(self, xml: str) -> XSDValidationResult:
        errors: list[XSDValidationError] = []

        try:
            xml_doc = etree.fromstring(xml.encode("utf-8"))
        except etree.XMLSyntaxError as e:
            errors.append(
                XSDValidationError(
                    message=str(e),
                    line=e.lineno,
                    column=e.position[1] if e.position else None,
                )
            )
            return XSDValidationResult(is_valid=False, errors=errors)

        is_valid = self._schema.validate(xml_doc)

        if not is_valid:
            for entry in self._schema.error_log:
                errors.append(
                    XSDValidationError(
                        message=entry.message,
                        line=entry.line,
                        column=entry.column,
                    )
                )

        return XSDValidationResult(is_valid=is_valid, errors=errors)
    
    def build_repair_prompt(
        xml: str,
        validation_result: XSDValidationResult
    ) -> str:
        errors = "\n".join(
            f"- {e.message}" for e in validation_result.errors
        )

        return f"""
Сформированный XML содержит ошибки:

{errors}

Исправь XML так, чтобы он соответствовал XSD-схеме.
Верни ТОЛЬКО исправленный XML.
"""



