import json

class Question:

    def __init__(self, position: int, title: str, text: str, image: str):
        self.position = position
        self.title = title
        self.text = text
        self.image = image

    def ConvertToJson(self):
        return json.dumps(self.__dict__)
