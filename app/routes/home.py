from flask import Blueprint, render_template, redirect, flash, url_for

home_bp = Blueprint('home',__name__)

@home_bp.route('/home',methods=['GET','POST'])
def view_home():
    return render_template('home.html')