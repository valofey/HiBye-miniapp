import json


class Event:
    def __init__(self, event_id, capacity, num_registered, description, join_url):
        self.event_id = event_id
        self.capacity = capacity
        self.num_registered = num_registered
        self.description = description
        self.join_url = join_url

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_string):
        data = json.loads(json_string)
        return cls(data["event_id"], data["capacity"], data["number_of_registered_peoples"], data["description"],
                   data["join_url"])
