from app.models.KnowledgeAreaDto import KnowledgeAreaDto
from app.models.tables import Definition


class DefinitionDto:
    def __init__(self, definition: Definition):
        self.content = definition.content
        self.knowledge_area = definition.knowledge_area
        self.order = definition.order

    def to_serializable(self):
        return {
            "content": self.content,
            "knowledge_area": KnowledgeAreaDto(self.knowledge_area).to_serializable(),
            "order": self.order
        }

    # content = db.Column(db.String(MAX_LENGTH['content']), nullable=False)
    # order = db.Column(db.Integer, nullable=False)
    # entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'))
    # knowledge_area_id = db.Column(db.Integer, db.ForeignKey('knowledge_area.id'))