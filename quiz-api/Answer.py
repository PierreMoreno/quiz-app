import json

class Answer:

    def __init__(self, text: str, id: int, isCorrect: bool):
        self.text = text
        self.id = id
        self.isCorrect = isCorrect

    def ConvertToJson(self):
        return {"text": self.text,"id": self.id, 'isCorrect': self.isCorrect}