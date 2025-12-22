from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import login_user, logout_user, current_user
from app.form import RegistrationForm, LoginForm 
from app.models import User
from app import bcrypt, db

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home.view_home')) # Redirect if already logged in
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if user exists using the email from form data
        user_exist = User.query.filter_by(email=form.email.data).first()
        if user_exist:
            flash('Email already exists. Please login.', 'danger')
            return redirect(url_for('auth.register'))
        
        # Hash password and create user
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()

        flash(f'Account created for {form.username.data}! You can now login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.view_home')) # Prevent double login
    
    form = LoginForm() # Create this class in form.py
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Verify hash against plain text attempt
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home.view_home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            
    return render_template('login.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))