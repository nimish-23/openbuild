from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField , TextAreaField , SelectField , DateField 
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired , Length , Email , EqualTo , Optional 
import datetime

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=4,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')

class ProjectForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired(),Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[DataRequired(),Length(max=1000)])
    status = SelectField('Current Status', choices=[
        ('ideation', 'Ideation'),
        ('in_progress', 'In Progress'),
        ('beta', 'Beta'),
        ('launched', 'Launched')
    ], default='in_progress')
    start_date = DateField('Start Date', format='%Y-%m-%d', default=datetime.date.today, validators=[Optional()])
    tech_stack = StringField('Tech Stack (e.g. Python, Flask, SQLite)', validators=[Optional()])
    repo_url = StringField('Git Repository Link', validators=[Optional()])
    submit = SubmitField('Create Project')

class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired(),Length(min=2,max=100)])
    content = TextAreaField('What did you build today ?',validators=[DataRequired()])
    image = FileField('Upload Screenshot (Optional)',validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    post_type = SelectField('Post Type',choices=[
        ('INIT'),
        ('FEATURE'),
        ('FIX'),
        ('REFACTOR'),
        ('DEPLOY'),
        ('REFLECTION'),
        ('UPDATE')
    ])
    submit = SubmitField('Post Update')