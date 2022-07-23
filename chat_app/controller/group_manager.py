#!/usr/bin/python3

from typing import Iterator
from chat_app.controller.controller_utils import handle_exception
from chat_app.controller.user_manager import is_user_group_admin
from chat_app.model.data import DB, Group, GroupMembers


def fetch_groups_by_uid(user_id:int) -> Iterator:
    groups = GroupMembers.query.filter_by(uid = user_id).all()
    return list(filter(None, map(lambda mapping:Group.query.get(mapping.gid), groups)))

def fetch_groups_by_gid(group_id:int) -> object:
    return Group.query.get(group_id)


def create_group(group_name:str, creator_id:int, description:str=None, group_users:list=[]) -> tuple:
    try:
        new_group = Group(name=group_name, description=description)
        group_users.append(creator_id)
        DB.session.add(new_group)
        DB.session.flush()
        for user_id in group_users:
            new_group_member = GroupMembers(gid=new_group.gid, uid=user_id, is_group_admin=user_id==creator_id)
            DB.session.add(new_group_member)
        DB.session.commit()
        return True, ""
    except Exception as e:
        return False, str(e)

@handle_exception
def update_group(group_id:int, user_id:int, group_name:str=None, description:str=None) ->None:
    group_entry = Group.query.get(group_id)
    group_entry.name = group_name
    group_entry.description = description
    DB.session.add(group_entry)
    DB.session.commit()
    return True, "Group updated successfully"
    

def delete_group(group_id:int, user_id:int) ->None:
    pass

def leave_group(group_id:int, user_id:int) ->None:
    pass

def add_users_to_group(group_id:int, curr_user_id:int, target_users_id_list:list[int], add_as_admin:bool=False) -> None:
    pass

@handle_exception
def add_user_to_group(group_id:int, curr_user_id:int, target_user_id:int, add_as_admin:bool=False) -> None:
    if not is_user_group_admin(user_id=curr_user_id, group_id=group_id):
        raise Exception(f"Current user has insufficient privilege")
    new_entry = GroupMembers(gid=group_id, uid=target_user_id, add_as_admin=False)
    DB.session.add(new_entry)
    DB.session.commit()
    return True, "User successfully added"

def remove_user_from_group(group_id:int, curr_user_id:int, target_user_id:int) -> None:
    pass

def make_user_group_admin(group_id:int, curr_user_id:int, target_user_id:int) -> None:
    pass

def revoke_group_admin_privileges(group_id:int, curr_user_id:int, target_user_id:int) -> None:
    pass
