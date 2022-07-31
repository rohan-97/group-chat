
import json
from flask import flash
from chat_app import app


def process_flash(result:bool, message:str) -> None:
    if message:
        flash(message, 'info' if result else 'danger')

def prepare_json_response(return_code:int=200, data:dict=None)->object:
    response = app.response_class(
        response=json.dumps(data),
        status=return_code,
        mimetype='application/json'
        )
    return response