from flask import flash, redirect, render_template, request, session
from chat_app import app
from chat_app.controller.user_manager import authenticate_user, get_user_info

@app.route("/", methods=["GET", "POST"])
def login_page():
    if request.method == "GET":
        if 'user_id' in session:
            return redirect('dashboard')
        return render_template("login.html")
    else:
        username=request.form.get('username')
        password=request.form.get('password')
        if not username:
            flash("username not provided", "danger")
            return redirect("/")
        if not password:
            flash("password not provided", "danger")
            return redirect("/")
        user_id = authenticate_user(username, password)
        if user_id is None:
            flash("Invalid credentials!", "danger")
            return redirect("/")
        u_info = get_user_info(user_id)
        session['user_id'] = user_id
        session['is_admin'] = u_info.is_admin
        session['user_name'] = u_info.name
        return redirect("/dashboard")

@app.route("/logout", methods=["GET"])
def logout():
    if 'user_id' in session:
        del session['user_id']
        del session['is_admin']
        del session['user_name']
    return redirect("/")