from app.models.tables import QuestionRepository


class QuestionDto:
    def __init__(self, question: QuestionRepository):
        self.statement = question.statement
        self.answer = question.answer
        self.explanation = question.explanation
        self.order = question.order

    def to_serializable(self):
        return self.__dict__

