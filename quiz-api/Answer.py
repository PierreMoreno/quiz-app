import json

class Answer:

    def init(self, text: str, question_id: int, is_correct: int):
        self.text = text
        self.question_id = question_id
        self.is_correct = is_correct

    def ConvertToJson(self):
        return json.dumps(self.__dict__)