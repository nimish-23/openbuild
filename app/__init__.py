import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# Load the variables from .env into the environment
load_dotenv()
bcrypt = Bcrypt()

# Fix typo: login_manager (common naming convention)
login_manager = LoginManager() 
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Read the secret key from the environment
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    
    # Crucial: Initialize login_manager with the app
    login_manager.init_app(app) 
    # Set the 'login' view for @login_required redirects
    login_manager.login_view = 'auth.login' 

    from app.routes.auth import auth
    app.register_blueprint(auth, url_prefix='/')

    from app.routes.home import home_bp
    app.register_blueprint(home_bp,url_prefix='/')

    return app