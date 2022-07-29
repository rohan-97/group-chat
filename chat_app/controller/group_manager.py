#!/usr/bin/python3

from typing import Iterator
from chat_app.controller.controller_utils import handle_exception
from chat_app.controller.user_manager import assert_user_is_group_admin, get_user_group_membership_details
from chat_app.model.data import DB, Group, GroupMembers


def fetch_groups_by_uid(user_id:int) -> Iterator:
    groups = GroupMembers.query.filter_by(uid = user_id).all()
    return list(filter(None, map(lambda mapping:Group.query.get(mapping.gid), groups)))

def fetch_groups_by_gid(group_id:int) -> object:
    return Group.query.get(group_id)


@handle_exception
def create_group(group_name:str, creator_id:int, description:str=None, group_users:list=[]) -> tuple:
    group_users.append(creator_id)
    new_group = Group(name=group_name, description=description)
    DB.session.add(new_group)
    DB.session.flush()
    for user_id in group_users:
        new_group_member = GroupMembers(gid=new_group.gid, uid=user_id, is_group_admin=user_id==creator_id)
        DB.session.add(new_group_member)
    DB.session.commit()
    return True, ""

@handle_exception
def update_group(group_id:int, user_id:int, group_name:str=None, description:str=None) -> tuple:
    group_entry = Group.query.get(group_id)
    group_entry.name = group_name
    group_entry.description = description
    DB.session.add(group_entry)
    DB.session.commit()
    return True, "Group updated successfully"
    

@handle_exception
def delete_group(group_id:int, user_id:int) -> tuple:
    assert_user_is_group_admin(user_id=user_id, group_id=group_id)

@handle_exception
def add_user_to_group(group_id:int, curr_user_id:int, target_user_id:int, add_as_admin:bool=False) -> tuple:
    assert_user_is_group_admin(user_id=curr_user_id, group_id=group_id)
    new_entry = GroupMembers(gid=group_id, uid=target_user_id)
    DB.session.add(new_entry)
    DB.session.commit()
    return True, "User successfully added"

@handle_exception
def remove_user_from_group(group_id:int, curr_user_id:int, target_user_id:int) -> tuple:
    if curr_user_id != target_user_id:
        assert_user_is_group_admin(user_id=curr_user_id, group_id=group_id)
    user_entry = GroupMembers.query.get((group_id, target_user_id))
    DB.session.delete(user_entry)
    DB.session.commit()
    return True, "Successfully Removed user"

@handle_exception
def set_group_admin_value(group_id:int, curr_user_id:int, target_user_id:int, group_admin:bool) -> tuple:
    assert_user_is_group_admin(user_id=curr_user_id, group_id=group_id)
    membership_details = get_user_group_membership_details(target_user_id, group_id)
    membership_details.is_group_admin = group_admin
    DB.session.add(membership_details)
    DB.session.commit()
    return True, "Successfully set user as admin"
