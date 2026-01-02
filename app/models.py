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

    tech_stack = db.Column(db.String(225))
    repo_url = db.Column(db.String(225))

    posts = db.relationship('Posts',backref='project', cascade="all, delete",lazy=True)

class Posts(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    project_id = db.Column(db.Integer,db.ForeignKey('projects.id'),nullable=False)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    post_type = db.Column(db.String(100),default='UPDATE')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    image_file = db.Column(db.String(20), nullable=True)
    author = db.relationship("Users", backref="posts")

