from flask import redirect, render_template, session
from chat_app import app
from chat_app.controller.group_manager import fetch_groups_by_uid

@app.route("/dashboard", methods=["GET"])
def dashboard_page():
    if 'user_id' not in session:
        return redirect("/")
    session_info = dict(session)
    user_groups = fetch_groups_by_uid(session.get('user_id'))
    return render_template("dashboard.html", session_data=session_info, groups=user_groups)