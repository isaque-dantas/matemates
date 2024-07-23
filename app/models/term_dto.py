from app.models.syllable_dto import SyllableDto
from app.models.tables import TermRepository


class TermDto:
    def __init__(self, term: TermRepository):
        self.content = term.content,
        self.gender = term.gender,
        self.grammatical_category = term.grammatical_category,
        self.is_main_term = term.is_main_term,
        self.order = term.order,
        self.syllables = term.syllables

    def to_serializable(self):
        return {
            "content": self.content,
            "gender": self.gender,
            "grammatical_category": self.grammatical_category,
            "is_main_term": self.is_main_term,
            "order": self.order,
            "syllables": list(map(lambda syllable: SyllableDto(syllable).to_serializable(), self.syllables))
        }
