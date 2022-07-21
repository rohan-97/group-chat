from flask import render_template, session
from chat_app import app

@app.route("/create_group")
def create_group_page():
    return render_template('new_group.html', session_data = dict(session))