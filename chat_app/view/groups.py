from django.shortcuts import render
from flask import flash, redirect, render_template, request, session
from chat_app import app
from chat_app.controller.group_manager import create_group, fetch_groups_by_gid
from chat_app.controller.user_manager import get_registered_users, get_users_from_group, get_users_which_are_not_in_group

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

@app.route("/edit_group/<int:group_id>", methods=["GET"])
def edit_group_page(group_id:int):
    group_info = fetch_groups_by_gid(group_id=group_id)
    users = get_users_from_group(group_id=group_id)
    users_not_in_group = get_users_which_are_not_in_group(group_id=group_id)
    return render_template("group_settings.html", session_data=dict(session), group=group_info, users=users, users_not_in_group=users_not_in_group)

@app.route("/group/<int:group_id>", methods=["GET"])
def group_chat_page(group_id:int):
    group_info = fetch_groups_by_gid(group_id=group_id)
    return render_template("group_chat_page.html", session_data=dict(session), group=group_info)