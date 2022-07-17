#!/usr/bin/python3

def create_message(user_id:int, group_id:int, message:str, likes:int=0) -> None:
    pass

def fetch_recent_messges(group_id:int, lower_limit:int, upper_limit:int) -> list:
    pass

def update_message(editor_id:int, message_id:int, message:str) -> None:
    pass

def delete_message(deletor_id:int, message_id:int) -> None:
    pass

def like_message(user_id:int, message_id:int)-> None:
    pass

def unlike_message(user_id:int, message_id:int)-> None:
    pass

def list_people_who_liked_message(message_id:int)-> list:
    pass