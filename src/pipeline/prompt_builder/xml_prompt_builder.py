from typing import List, Optional
from pipeline.types import ParsedBlock
from pipeline.xsd.types import XSDContext, XSDElement



class XMLPromptBuilder:
    def __init__(
        self,
        xml_schema_name: str,
        xsd_context: Optional[XSDContext] = None,
        language: str = "ru",
        strict: bool = True,
    ):
        self.xml_schema_name = xml_schema_name
        self.xsd_context = xsd_context
        self.language = language
        self.strict = strict


    def build(self, blocks: List[ParsedBlock]) -> str:
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(blocks)

        return system_prompt + "\n\n" + user_prompt

    
    def _build_system_prompt(self) -> str:
        parts: list[str] = []

        parts.append(
            f"""
Ты — интеллектуальная система генерации XML-документов
для строительной отрасли Российской Федерации.

Твоя задача:
- извлечь структурированные данные из входного документа;
- сформировать корректный XML-документ;
- строго соблюдать иерархию и структуру XML.

Требования:
1. Формируй ТОЛЬКО XML, без поясняющего текста.
2. XML должен соответствовать XSD-схеме: {self.xml_schema_name}.
3. Используй только данные, явно присутствующие во входных данных.
4. Если данные отсутствуют — не выдумывай значения.
5. Сохраняй числовые значения без изменений.
6. Язык значений — {self.language}.
""".strip()
        )

        if self.strict:
            parts.append(
                """
7. Не добавляй теги, отсутствующие в XSD-схеме.
8. Соблюдай обязательность элементов (required / optional).
""".strip()
            )

        if self.xsd_context:
            parts.append(self._build_xsd_rules())

        parts.append(
            """
Каждый XML-элемент должен иметь атрибут source,
указывающий идентификатор блока, из которого было извлечено значение.

Формат:
<Tag source="block_id">value</Tag>
""".strip()
        )

        return "\n\n".join(parts)

    
    def _build_user_prompt(self, blocks: List[ParsedBlock]) -> str:
        parts: list[str] = []

        parts.append("ВХОДНЫЕ ДАННЫЕ ДОКУМЕНТА:")

        for block in blocks:
            parts.append(
                f"""
[BLOCK_ID: {block.block_id}]
[TYPE: {block.type}]
[SOURCE: {block.source}]
CONTENT:
{block.content}
""".strip()
            )

        parts.append(
            """
На основе приведённых данных сформируй XML-документ,
строго следуя ограничениям XSD.
""".strip()
        )

        return "\n\n".join(parts)

    
    def _build_xsd_rules(self) -> str:
        assert self.xsd_context is not None

        lines: list[str] = []
        lines.append("Ограничения и структура XML (на основе XSD):")

        for el in self.xsd_context.elements:
            lines.append(self._format_xsd_element(el))

        return "\n".join(lines)
    
    def _format_xsd_element(self, el: XSDElement) -> str:
        parts = []

        parts.append(f"- <{el.name}>")

        parts.append(f"  тип: {el.type}")

        if el.required:
            parts.append("  обязательный")
        else:
            parts.append("  необязательный")

        if el.description:
            parts.append(f"  описание: {el.description}")

        if el.restrictions:
            parts.append(
                "  ограничения: " + ", ".join(el.restrictions)
            )

        return " | ".join(parts)


