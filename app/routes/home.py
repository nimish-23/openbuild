from flask import Blueprint, render_template, request, make_response
from flask_login import current_user
from app.models import Posts
import logging

home_bp = Blueprint('home', __name__)
logger = logging.getLogger(__name__)

@home_bp.route('/', methods=['GET'])
def view_home():
    page = request.args.get('page', 1, type=int)

    posts = Posts.query.order_by(Posts.created_at.desc()) \
                       .paginate(page=page, per_page=5, error_out=False)
    
    # Debug: Log request details
    is_htmx = request.headers.get('HX-Request')
    logger.info(f"Request - Page: {page}, HTMX: {is_htmx}, Has Next: {posts.has_next}, Total Posts: {posts.total}")
    print(f"[DEBUG] Request - Page: {page}, HTMX: {is_htmx}, Has Next: {posts.has_next}, Total Posts: {posts.total}")
    
    # Handle HTMX requests for infinite scroll - return only the feed items
    if is_htmx:
        print(f"[DEBUG] Returning HTMX partial for page {page}")
        return render_template('partials/_feed_items.html', posts=posts)

    # Regular page load - return full template
    return render_template('home.html', posts=posts)
