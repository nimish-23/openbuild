from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import login_required , current_user

home_bp = Blueprint('home',__name__)

@home_bp.route('/home',methods=['GET','POST'])
def view_home():
    return render_template('home.html')


@home_bp.route('/',methods=['GET'])
def landing_page():
    
    return render_template('landing_page.html')