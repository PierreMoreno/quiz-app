import json

class ParticipationAnswer:

    def __init__(self, participation_id: int, answer_id):
        self.participation_id = participation_id
        self.answer_id = answer_id

    def ConvertToJson(self):
        return json.dumps(self.__dict__)
