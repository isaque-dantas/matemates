from app.models.tables import KnowledgeArea


class KnowledgeAreaDto:
    def __init__(self, knowledge_area: KnowledgeArea):
        self.content = knowledge_area.content
        self.subject = knowledge_area.subject

    def to_serializable(self):
        return {
            "content": self.content,
            "subject": self.subject
        }
