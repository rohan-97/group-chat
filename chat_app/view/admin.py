from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from chat_app.model.data import *
from chat_app import app
"""
For addition of user and user modification, we are leveraging flask-admin panel
This panel allows us to add user with specific attributes and presents a UI for the same.
we are just linking the admin UI to main page dashboard
"""
admin = Admin(app)
admin.add_view(ModelView(User, DB.session))