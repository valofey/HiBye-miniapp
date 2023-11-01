from enum import Enum, auto


class Functions(Enum):
    GET_USER = auto()
    GET_USERS = auto()
    GET_MEETINGS = auto()
    REGISTER_USER = auto()
    UPDATE_USER = auto()
    REGISTER_TO_MEETING = auto()
    CREATE_MEETING = auto()
    CREATE_FAST_MEETING = auto()
    GET_EVENTS = auto()

    @classmethod
    def from_string(cls, string):
        try:
            return cls[string.upper()]
        except KeyError:
            raise ValueError(f"Invalid Functions: {string}")
