from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from chat_app.model.data import *
from chat_app import app

class GroupMembersModelView(ModelView):
    column_list = ['gid', 'uid', 'is_group_admin']

admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Group, db.session))
admin.add_view(GroupMembersModelView(GroupMembers, db.session))
admin.add_view(ModelView(Messages, db.session))
admin.add_view(ModelView(MessageLikeMap, db.session))