from lxml import etree
from pathlib import Path
from typing import Optional

from .types import XSDElement, XSDContext


XSD_NS = {
    "xs": "http://www.w3.org/2001/XMLSchema"
}


class XSDParser:
    def __init__(self, xsd_path: str):
        self.xsd_path = Path(xsd_path)

        if not self.xsd_path.exists():
            raise FileNotFoundError(f"XSD file not found: {xsd_path}")

        self.tree = etree.parse(str(self.xsd_path))
        self.root = self.tree.getroot()

    def parse(self) -> XSDContext:
        schema_name = self.xsd_path.name
        target_ns = self.root.get("targetNamespace")

        elements: list[XSDElement] = []

        for elem in self.root.xpath(".//xs:element", namespaces=XSD_NS):
            xsd_element = self._parse_element(elem)
            if xsd_element:
                elements.append(xsd_element)

        return XSDContext(
            schema_name=schema_name,
            target_namespace=target_ns,
            elements=elements
        )
    
    def _parse_element(self, elem) -> Optional[XSDElement]:
        name = elem.get("name")
        if not name:
            return None

        type_ = elem.get("type", "string")

        min_occurs = elem.get("minOccurs", "1")
        required = min_occurs != "0"

        description = self._extract_annotation(elem)
        restrictions = self._extract_restrictions(elem)

        return XSDElement(
            name=name,
            type=type_,
            required=required,
            description=description,
            restrictions=restrictions
        )
    
    def _extract_annotation(self, elem) -> Optional[str]:
        docs = elem.xpath(
            ".//xs:annotation/xs:documentation",
            namespaces=XSD_NS
        )

        if not docs:
            return None

        return " ".join(d.text.strip() for d in docs if d.text)
    
    def _extract_restrictions(self, elem) -> Optional[list[str]]:
        restrictions = []

        restriction_nodes = elem.xpath(
            ".//xs:restriction/*",
            namespaces=XSD_NS
        )

        for r in restriction_nodes:
            tag = etree.QName(r).localname
            value = r.get("value")
            if value:
                restrictions.append(f"{tag}={value}")

        return restrictions or None



