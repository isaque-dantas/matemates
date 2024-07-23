from app.models.tables import Image


class ImageDto:
    def __init__(self, image: Image):
        self.path = image.path,
        self.caption = image.caption,
        self.order = image.order

    def to_serializable(self):
        return self.__dict__
