from email.policy import default
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from chat_app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messaging.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'test1234'

db = SQLAlchemy(app)

class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

class Group(db.Model):
    gid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text)

class GroupMembers(db.Model):
    gid = db.Column(db.Integer, ForeignKey(User.__table__.c['uid']), primary_key=True)
    uid = db.Column(db.Integer, ForeignKey(Group.__table__.c['gid']), primary_key=True)
    is_group_admin = db.Column(db.Boolean, default=False)

class Messages(db.Model):
    msgid = db.Column(db.Integer, primary_key=True) 
    gid = db.Column(db.Integer, ForeignKey(User.__table__.c['uid']), nullable=False)
    uid = db.Column(db.Integer, ForeignKey(Group.__table__.c['gid']), nullable=False)
    message = db.Column(db.Text, nullable=False)
    send_time = db.Column(db.DateTime, primary_key=True, nullable=False)
