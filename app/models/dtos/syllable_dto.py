from app.models.tables import SyllableRepository


class SyllableDto:
    def __init__(self, syllable: SyllableRepository):
        self.content = syllable.content,
        self.order = syllable.order

    def to_serializable(self):
        return self.__dict__
