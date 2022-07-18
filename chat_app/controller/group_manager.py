#!/usr/bin/python3

from typing import Iterator
from chat_app.model.data import GroupMembers


def fetch_groups_by_uid(user_id:int) -> Iterator:
    return GroupMembers.query.filter_by(uid = user_id)

def create_group(group_name:str, creator_id:int, description:str=None) -> None:
    pass

def update_group(group_id:int, user_id:int, group_name:str=None, description:str=None) ->None:
    pass

def delete_group(group_id:int, user_id:int) ->None:
    pass

def leave_group(group_id:int, user_id:int) ->None:
    pass

def add_users_to_group(group_id:int, curr_user_id:int, target_users_id_list:list[int], add_as_admin:bool=False) -> None:
    pass

def add_user_to_group(group_id:int, curr_user_id:int, target_user_id:int, add_as_admin:bool=False) -> None:
    pass

def remove_user_from_group(group_id:int, curr_user_id:int, target_user_id:int) -> None:
    pass

def make_user_group_admin(group_id:int, curr_user_id:int, target_user_id:int) -> None:
    pass

def revoke_group_admin_privileges(group_id:int, curr_user_id:int, target_user_id:int) -> None:
    pass
