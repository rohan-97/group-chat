from flask import redirect, render_template, session
from chat_app import app
from chat_app.view.utils import requires_user_session

@app.route("/dashboard", methods=["GET"])
def dashboard_page():
    if 'user_id' not in session:
        return redirect("/")
    session_info = dict(session)
    return render_template("dashboard.html", session_data=session_info)