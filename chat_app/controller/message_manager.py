#!/usr/bin/python3

from datetime import datetime

from sqlalchemy import desc
from chat_app.controller.controller_utils import handle_exception
from chat_app.controller.user_manager import assert_user_is_group_admin
from chat_app.model.data import DB, Messages

@handle_exception
def create_message(user_id:int, group_id:int, message:str, likes:int=0) -> tuple:
    msg_obj = Messages(gid=group_id, uid=user_id, message=message, send_time=datetime.now())
    DB.session.add(msg_obj)
    DB.session.commit()
    return True, "Message successfully send!"

@handle_exception
def fetch_recent_messages(group_id:int, records:int, page_no:int) -> tuple:
    return True, Messages.query.filter_by(gid=group_id).order_by(desc(Messages.send_time)).limit(records).offset(records*page_no).all()

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