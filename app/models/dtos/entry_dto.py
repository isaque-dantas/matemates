from app.models.dtos.definition_dto import DefinitionDto
from app.models.dtos.image_dto import ImageDto
from app.models.dtos.question_dto import QuestionDto
from app.models.tables import EntryRepository
from app.models.dtos.term_dto import TermDto


class EntryDto:
    def __init__(self, entry: EntryRepository):
        self.content: str = entry.content
        self.is_validated: bool = entry.is_validated
        self.images = entry.images
        self.questions = entry.questions
        self.definitions = entry.definitions
        self.terms = entry.terms

    def to_serializable(self):
        self.images = list(map(lambda image: ImageDto(image).to_serializable(), self.images))
        self.questions = list(map(lambda question: QuestionDto(question).to_serializable(), self.questions))
        self.definitions = list(map(lambda definition: DefinitionDto(definition).to_serializable(), self.definitions))
        self.terms = list(map(lambda term: TermDto(term).to_serializable(), self.terms))

        return self.__dict__
