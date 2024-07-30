from app.models.tables import KnowledgeAreaRepository


class KnowledgeAreaDto:
    def __init__(self, knowledge_area: KnowledgeAreaRepository):
        self.content = knowledge_area.content
        self.subject = knowledge_area.subject

    def to_serializable(self):
        return {
            "content": self.content,
            "subject": self.subject
        }
