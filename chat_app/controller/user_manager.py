#!/usr/bin/python3

from chat_app.model.data import User


def authenticate_user(username:str, password:str) -> int:
    """
    Authenticates user and returns user id after successful auth.

    :param username: unique username
    :type username: str
    :param password: password of user
    :type password: str
    :return: user id if the authentication is successful otherwise None in case of failure
    :rtype: int
    """
    user = User.query.filter_by(username=username).first()
    return user.uid if user and user.password == password else None

def get_registered_users() -> list[object]:
    return User.query.all()

def get_registered_users_id() -> list[int]:
    return list(map(lambda user:user.uid, get_registered_users()))

def get_user_info(user_id:int) -> object:
    return User.query.get(user_id)