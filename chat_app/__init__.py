from flask import Flask, session
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

from chat_app.view import admin
from chat_app.view import auth
from chat_app.view import dashboard
from chat_app.view import groups
from chat_app.view import messages