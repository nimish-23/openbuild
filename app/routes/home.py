from flask import Blueprint, render_template, request
from flask_login import current_user
from app.models import Posts

home_bp = Blueprint('home', __name__)

@home_bp.route('/', methods=['GET'])
def view_home():
    page = request.args.get('page', 1, type=int)

    posts = Posts.query.order_by(Posts.created_at.desc()) \
                       .paginate(page=page, per_page=5)

    return render_template('home.html', posts=posts)
