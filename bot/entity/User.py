import json

class User:
    def __init__(self, user_id, telegram_id, name, description, telegram_name):
        self.user_id = user_id
        self.telegram_id = telegram_id
        self.name = name
        self.description = description
        self.telegram_name = telegram_name

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_string):
        data = json.loads(json_string)
        return cls(data["user_id"], data["telegram_id"], data["name"], data["description"], data["telegram_name"])

    def __str__(self):
        return f"*{self.name}*, Возраст: {self.age}\n\n{self.user_info}\n\n*Пишите в Telegram: @{self.telegram_name}*"
