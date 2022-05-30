import json

class Participation:

    def __init__(self, player: str):
        self.player = player

    def ConvertToJson(self):
        return json.dumps(self.__dict__)
