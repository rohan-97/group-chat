from flask import redirect, render_template, request, url_for
from chat_app import app
from chat_app.model.data import User, db

@app.route("/debug", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('index.html')
    else:
        us1 = User(
            username=request.form.get('username'),
            password=request.form.get('password'),
            name=request.form.get('name')
            )
        db.session.add(us1)
        db.session.commit()
        return render_template('index.html')
