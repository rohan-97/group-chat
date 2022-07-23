#!/usr/bin/python3

from chat_app.model.data import GroupMembers, User


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

def get_users_from_group(group_id:int) -> list:
    user_list = GroupMembers.query.filter_by(gid=group_id).all()
    return [(User.query.get(user.uid), user.is_group_admin) for user in user_list]

def get_users_which_are_not_in_group(group_id:int) -> list:
    present_user_set = set([user.uid for user in GroupMembers.query.filter_by(gid=group_id).all()])
    return filter(lambda user: user.uid not in present_user_set, get_registered_users())

def get_registered_users_id() -> list[int]:
    return list(map(lambda user:user.uid, get_registered_users()))

def get_user_info(user_id:int) -> object:
    return User.query.get(user_id)