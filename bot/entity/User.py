import json


class User:
    def __init__(self, user_id=None, name=None, description=None, photo_link=None):
        self.user_id = user_id
        self.name = name
        self.description = description
        self.photo_link = photo_link

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_string):
        data = json.loads(json_string)
        return cls(data["user_id"], data["name"], data["description"], data["photo_link"])

    # def __str__(self):
    #     return f"*{self.name}*, Возраст: {self.age}\n\n{self.user_info}\n\n*Пишите в Telegram: @{self.telegram_name}*"
