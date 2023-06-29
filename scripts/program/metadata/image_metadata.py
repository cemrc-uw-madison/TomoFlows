import json
from typing import List, Dict

class ImageSet:
    """
    An ImageSet describes the set of images that could be in a tilt-series or other grouping.
    """

    def __init__(self, header: Dict[str, str], images: List[str]):
        self.header = header
        self.images = images

class ImageMetadata:
    """
    Describes the imported datasets.
    """

    def __init__(self):
        self.image_sets: List[ImageSet] = []

    def add_image_set(self, image_set: ImageSet):
        self.image_sets.append(image_set)

    def save_to_json(self, filename: str):
        data = {
            "image_sets": self.image_sets
        }

        with open(filename, "w") as file:
            json.dump(data, file, indent=4, cls=ImageSetEncoder)

    @classmethod
    def load_from_json(cls, filename: str) -> "ImageMetadata":
        with open(filename, "r") as file:
            data = json.load(file)

        image_data = cls()
        image_data.image_sets = data["image_sets"]

        return image_data

class ImageSetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ImageSet):
            return {
                "header": obj.header,
                "images": obj.images
            }
        return super().default(obj)