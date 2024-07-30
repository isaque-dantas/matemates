from app.models.dtos.knowledge_area_dto import KnowledgeAreaDto
from app.models.tables import DefinitionRepository


class DefinitionDto:
    def __init__(self, definition: DefinitionRepository):
        self.content = definition.content
        self.knowledge_area = definition.knowledge_area
        self.order = definition.order

    def to_serializable(self):
        return {
            "content": self.content,
            "knowledge_area": KnowledgeAreaDto(self.knowledge_area).to_serializable(),
            "order": self.order
        }
