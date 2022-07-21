from email.policy import default
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from chat_app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messaging.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'test1234'

DB = SQLAlchemy(app)

class User(DB.Model):
    uid = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(20), unique=True, nullable=False)
    password = DB.Column(DB.String(20), nullable=False)
    name = DB.Column(DB.String(20), nullable=False)
    is_admin = DB.Column(DB.Boolean, default=False, nullable=False)

class Group(DB.Model):
    gid = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(20), nullable=False)
    description = DB.Column(DB.Text)

class GroupMembers(DB.Model):
    gid = DB.Column(DB.Integer, ForeignKey(User.__table__.c['uid']), primary_key=True)
    uid = DB.Column(DB.Integer, ForeignKey(Group.__table__.c['gid']), primary_key=True)
    is_group_admin = DB.Column(DB.Boolean, default=False)

class Messages(DB.Model):
    msgid = DB.Column(DB.Integer, primary_key=True) 
    gid = DB.Column(DB.Integer, ForeignKey(User.__table__.c['uid']), nullable=False)
    uid = DB.Column(DB.Integer, ForeignKey(Group.__table__.c['gid']), nullable=False)
    message = DB.Column(DB.Text, nullable=False)
    send_time = DB.Column(DB.DateTime, primary_key=True, nullable=False)

class MessageLikeMap(DB.Model):
    msgid = DB.Column(DB.Integer, ForeignKey(Messages.__table__.c['msgid']), primary_key=True)
    uid = DB.Column(DB.Integer, ForeignKey(Group.__table__.c['gid']), primary_key=True)

DB.create_all()