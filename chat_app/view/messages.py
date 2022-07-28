import datetime
from tokenize import group
from flask import request, session
from chat_app import app
from chat_app.controller.message_manager import create_message, fetch_recent_messages, like_message, list_people_who_liked_message, unlike_message
from chat_app.controller.user_manager import get_user_info, is_user_part_of_group
from chat_app.view.utils import prepare_json_response

@app.route('/api/message', methods=["POST"])
def message_manager():
    if request.method == "POST":
        message = request.json.get('message')
        user_id = request.json.get('user_id')
        group_id = request.json.get('group_id')
        res, message = create_message(user_id=user_id, group_id=group_id, message=message)
        return prepare_json_response(200 if res else 400, {"message":message})

@app.route('/api/message/<int:group_id>/<int:page_number>', methods=["GET"])
def get_messages(group_id:int, page_number:int=0):
    if not is_user_part_of_group(session.get('user_id'), group_id):
        return prepare_json_response(401, "User is not part of group")
    res, messages = fetch_recent_messages(group_id=group_id, records=3, page_no=page_number)
    if not res:
        return prepare_json_response(400, messages)
    response = []
    for msg in messages:
        resp_element = {}
        resp_element["msg_id"] = msg.msgid
        resp_element["message"] = msg.message
        resp_element["timestamp"] = msg.send_time.timestamp()
        resp_element["user_id"] = msg.uid
        resp_element["user_name"] = get_user_info(msg.uid).name
        resp_element["like_count"] = 0
        resp_element["show_like"] = True
        result, people = list_people_who_liked_message(msg.msgid)
        if result:
            resp_element["like_count"] = len(people)
            resp_element["show_like"] = session.get('user_id') not in [i.uid for i in people]
        response.append(resp_element)

    return prepare_json_response(200, response)

@app.route("/api/likemsg", methods=["POST", "DELETE"])
def like_user_message():
    user_id = request.json.get("user_id")
    message_id = request.json.get("message_id")
    if not user_id:
        return prepare_json_response(400, "Invalid input user_id field is empty")
    if not message_id:
        return prepare_json_response(400, "Invalid input message_id field is empty")
    if request.method == "POST":
        res, msg = like_message(message_id=message_id, user_id=user_id)
    if request.method == "DELETE":
        res, msg = unlike_message(message_id=message_id, user_id=user_id)
    return prepare_json_response(200 if res else 400, {"message":msg})
