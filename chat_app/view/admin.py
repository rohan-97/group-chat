from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from chat_app.model.data import *
from chat_app import app

class GroupMembersModelView(ModelView):
    column_list = ['gid', 'uid', 'is_group_admin']

class UserModelView(ModelView):
    column_list = ['uid', 'username', 'password', 'name', 'is_admin']

class GroupModelView(ModelView):
    column_list = ['gid', 'name', 'description']

class MessageLikeMapModelView(ModelView):
    column_list = ['msgid', 'uid']

admin = Admin(app)
admin.add_view(UserModelView(User, DB.session))
admin.add_view(GroupModelView(Group, DB.session))
admin.add_view(GroupMembersModelView(GroupMembers, DB.session))
admin.add_view(ModelView(Messages, DB.session))
admin.add_view(MessageLikeMapModelView(MessageLikeMap, DB.session))