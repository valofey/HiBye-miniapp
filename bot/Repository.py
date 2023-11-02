import random

from entity.User import User

users = dict()
users_already_met = dict()


def register_new_user(user: User):
    users[user.user_id] = user
    users_already_met[user.user_id] = set()


def get_user(user_id) -> User:
    return users[user_id]


def update_user(user_id, user_data) -> None:
    user = users[user_id]
    user.name = user_data['name']
    user.description = user_data['description']


def find_pair(user_id) -> int:
    remaining_keys = set(users.keys()) - users_already_met[user_id]
    random_user_id = random.choice(list(remaining_keys))
    users_already_met[user_id].add(random_user_id)
    users_already_met[random_user_id].add(user_id)
    return user_id
