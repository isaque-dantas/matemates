import json

from app.models.definition_dto import DefinitionDto
from app.models.image_dto import ImageDto
from app.models.question_dto import QuestionDto
from app.models.tables import EntryRepository
from app.models.term_dto import TermDto


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

        print(self.__dict__)

        return self.__dict__

        # return {
        #     "content": self.content,
        #     "is_validated": self.is_validated,
        #     "images": self.images,
        #     "questions": self.questions,
        #     "definitions": self.definitions,
        #     "terms": self.terms
        # }

# id = db.Column(db.Integer, primary_key=True, autoincrement=True)
# content = db.Column(db.String(256), nullable=False, unique=True)
# gender = db.Column(db.Enum('M', 'F'), nullable=True)
# grammatical_category = db.Column(
#     db.Enum('substantivo', 'verbo', 'adjetivo', 'numeral'), nullable=True
# )
# is_main_term = db.Column(db.Boolean, nullable=False, default=False)
# order = db.Column(db.Integer, nullable=False)
# 
# syllables = db.relationship('Syllable', backref='term')
# entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'))
