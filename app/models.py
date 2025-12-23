from app import db , login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model,UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100),unique=True,nullable=False)
    password = db.Column(db.String(100),nullable=False)

    #user(one) -> projects(many)
    projects = db.relationship('Projects',backref='owner',lazy=True)

class Projects(db.Model):

    __tablename__ = 'projects'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100),nullable=False)
    description = db.Column(db.String(1000))
    status = db.Column(db.String(100),default='in_progress')

    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

