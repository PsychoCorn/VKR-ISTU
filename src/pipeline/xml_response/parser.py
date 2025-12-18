from lxml import etree
from typing import Optional

from .types import XMLNode, XMLParseResult

class XMLResponseParser:
    def __init__(self, strict: bool = True):
        self.strict = strict

    def parse(self, xml_text: str) -> XMLParseResult:
        cleaned_xml = self._extract_xml(xml_text)

        try:
            root = etree.fromstring(cleaned_xml.encode("utf-8"))
        except etree.XMLSyntaxError as e:
            raise ValueError(f"Invalid XML from LLM: {e}")

        nodes: list[XMLNode] = []

        for elem in root.iter():
            if elem is root:
                continue

            nodes.append(
                XMLNode(
                    tag=elem.tag,
                    value=(elem.text or "").strip(),
                    source=elem.attrib.get("source")
                )
            )

        return XMLParseResult(
            nodes=nodes,
            raw_xml=cleaned_xml
        )
    
    def _extract_xml(self, text: str) -> str:
        text = text.strip()

        # Если LLM завернул XML в ```xml ... ```
        if text.startswith("```"):
            text = text.strip("`")
            text = text.replace("xml", "", 1).strip()

        # Пробуем вырезать XML-блок
        start = text.find("<")
        end = text.rfind(">")

        if start == -1 or end == -1:
            raise ValueError("No XML found in LLM response")

        return text[start:end + 1]
    
    

