#!/usr/bin/python3

def fetch_groups_by_uid(uid:int) -> list:
    pass

def create_group(group_name:str, creator_id:int, description:str=None) -> None:
    pass

def update_group(group_id:int, user_id:int, group_name:str=None, description:str=None) ->None:
    pass

def delete_group(group_id:int, user_id:int) ->None:
    pass

def add_user_to_group(group_id:int, curr_user_id:int, target_user_id:int, add_as_admin:bool=False) -> None:
    pass
