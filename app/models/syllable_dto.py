from app.models.tables import Syllable


class SyllableDto:
    def __init__(self, syllable: Syllable):
        self.content = syllable.content,
        self.order = syllable.order

    def to_serializable(self):
        return self.__dict__
