from django.shortcuts import render
from flask import flash, redirect, render_template, request, session
from chat_app import app
from chat_app.controller.group_manager import create_group
from chat_app.controller.user_manager import get_registered_users

@app.route("/create_group", methods=["GET", "POST"])
def create_group_page():
    if request.method == "GET":
        return render_template('new_group.html', session_data = dict(session), registered_users = get_registered_users())
    else:
        group_name = request.form.get("groupname")
        group_desc = request.form.get("groupdesc")
        # group_icon = request.form.get("group_icon")
        members = request.form.getlist("members")
        res, message = create_group(group_name, session.get("user_id"), group_desc, members)
        if message:
            flash(message, "info" if res else "danger")
        return redirect('/dashboard')

@app.route("/group/<int:group_id>", methods=["GET"])
def group_chat_page(group_id:int):
    return render_template("group_chat_page.html", session_data=dict(session), group_id=group_id)
