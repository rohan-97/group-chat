from flask import Flask
app = Flask(__name__)

from chat_app.view import dev
from chat_app.view import admin