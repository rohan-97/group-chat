from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from chat_app.model.data import *
from chat_app import app

class GroupMembersModelView(ModelView):
    column_list = ['gid', 'uid', 'is_group_admin']

admin = Admin(app)
admin.add_view(ModelView(User, DB.session))
admin.add_view(ModelView(Group, DB.session))
admin.add_view(GroupMembersModelView(GroupMembers, DB.session))
admin.add_view(ModelView(Messages, DB.session))
admin.add_view(ModelView(MessageLikeMap, DB.session))