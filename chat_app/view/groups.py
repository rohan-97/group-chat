from django.shortcuts import render
from flask import flash, redirect, render_template, request, session, url_for
from chat_app import app
from chat_app.controller.group_manager import add_user_to_group, create_group, fetch_groups_by_gid, remove_user_from_group, set_group_admin_value, update_group
from chat_app.controller.user_manager import get_registered_users, get_users_from_group, get_users_which_are_not_in_group, is_user_group_admin
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

@app.route("/edit_group/<int:group_id>", methods=["GET", "POST"])
def edit_group_page(group_id:int):
    if request.method == "GET":
        group_info = fetch_groups_by_gid(group_id=group_id)
        users = get_users_from_group(group_id=group_id)
        users_not_in_group = get_users_which_are_not_in_group(group_id=group_id)
        is_curr_user_group_admin = is_user_group_admin(session.get('user_id'), group_id=group_id)
        return render_template("group_settings.html", session_data=dict(session), group=group_info,
                users=users, users_not_in_group=users_not_in_group, 
                is_current_user_admin= is_curr_user_group_admin,
                is_user_group_admin=is_user_group_admin)
    else:
        print(f"Here")
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
    uid = request.json.get('user_id')
    group_id = request.json.get('group_id')
    if request.method == "POST":
        res, message = add_user_to_group(group_id, session.get('user_id'), uid)
    else:
        res, message = remove_user_from_group(group_id, session.get('user_id'), int(uid))
    return prepare_json_response(200 if res else 400, {"message":message})

@app.route("/api/usergroup/admin", methods=["POST"])
def toggle_group_admin_privileges():
    uid = request.json.get('user_id')
    group_id = request.json.get('group_id')
    is_group_admin = request.json.get('is_group_admin')
    print(f"ROhan Debug : {uid} : uid group id {group_id}")
    res, message = set_group_admin_value(group_id, session.get('user_id'), uid, not is_group_admin)
    if res:
        if is_group_admin:
            message = "Successfully revoked group admin privileges from user"
        else:
            message = "Successfully added group admin privileges to user"
    else:
        message = f"Error: {message}"
    
    return prepare_json_response(200 if res else 400, {"message":message})


