from django.shortcuts import render
from flask import flash, redirect, render_template, request, session, url_for
from chat_app import app
from chat_app.controller.group_manager import add_user_to_group, create_group, fetch_groups_by_gid, update_group
from chat_app.controller.user_manager import get_registered_users, get_users_from_group, get_users_which_are_not_in_group
from chat_app.view.utils import prepare_json_response, process_flash

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
        process_flash(res, message)
        return redirect('/dashboard')

@app.route("/edit_group/<int:group_id>", methods=["GET", "PUT"])
def edit_group_page(group_id:int):
    if request.method == "GET":
        group_info = fetch_groups_by_gid(group_id=group_id)
        users = get_users_from_group(group_id=group_id)
        users_not_in_group = get_users_which_are_not_in_group(group_id=group_id)
        return render_template("group_settings.html", session_data=dict(session), group=group_info, users=users, users_not_in_group=users_not_in_group)
    else:
        grp_name = request.form.get("groupname")
        grp_description = request.form.get("groupdesc")
        if not grp_name:
            flash("Group name not present", "danger")
            return redirect(url_for('edit_group_page', group_id=group_id))
        res, msg = update_group(group_id=group_id, user_id=session.get('user_id'), group_name=grp_name, description=grp_description)
        process_flash(res, msg)
        return redirect(url_for('edit_group_page', group_id=group_id))

@app.route("/group/<int:group_id>", methods=["GET"])
def group_chat_page(group_id:int):
    group_info = fetch_groups_by_gid(group_id=group_id)
    return render_template("group_chat_page.html", session_data=dict(session), group=group_info)


@app.route("/api/usergroup/manage", methods=["POST", "DELETE"])
def manage_group_user():
    if request.method == "POST":
        uid = request.json.get('user_id')
        group_id = request.json.get('group_id')
        res, message = add_user_to_group(group_id, session.get('user_id'), uid)
        return prepare_json_response(200 if res else 400, {"message":message})
