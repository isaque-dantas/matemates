from app.models.tables import ImageRepository


class ImageDto:
    def __init__(self, image: ImageRepository):
        self.path = image.path,
        self.caption = image.caption,
        self.order = image.order

    def to_serializable(self):
        return self.__dict__
