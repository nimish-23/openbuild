from flask import Blueprint , render_template , redirect , url_for , flash , request
from flask_login import login_required , current_user
from app.form import PostForm
from app import db
from app.models import Projects , Posts
import os
import secrets
from flask import current_app

post_bp = Blueprint('post',__name__)

def save_post_thumbnail(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    # Ensure this folder exists: app/static/post_images/
    picture_path = os.path.join(current_app.root_path, 'static/uploads', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@post_bp.route('/project/<int:project_id>/post/new',methods=['GET','POST'])
@login_required
def post_new(project_id):
    project = Projects.query.get_or_404(project_id)

    if project.user_id != current_user.id:
        flash("Unauthorized", "danger")
        return redirect(url_for('project.view_projects'))

    form = PostForm()
    if form.validate_on_submit():
        post_exists = Posts.query.filter_by(
            title=form.title.data, 
            project_id=project.id
        ).first()

        if post_exists:
            flash('A post with this title already exists for this project.', 'warning')
            return redirect(url_for('post.post_new',project_id=project.id))

        image_file = None
        if form.image.data:
            image_file = save_post_thumbnail(form.image.data)

        new_post = Posts(
            title=form.title.data,
            content=form.content.data,
            image_file=image_file,
            project_id=project.id,
            user_id=current_user.id,
            post_type=form.post_type.data
        )

        db.session.add(new_post)
        db.session.commit()
        flash('Update added successfully!', 'success')
        return redirect(url_for('project.project_details', project_id=project.id))

    return render_template('create_post.html', form=form, project=project)

@post_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def post_edit(post_id):
    post = Posts.query.get_or_404(post_id)

    # Security: Ensure only the author can edit
    if post.user_id != current_user.id:
        flash("You cannot edit this post!", "danger")
        return redirect(url_for('project.project_details', project_id=post.project_id))
    
    form = PostForm()
    
    if form.validate_on_submit():
        # Directly update fields without redundant title checks
        post.title = form.title.data
        post.content = form.content.data
        post.post_type = form.post_type.data

        # Handle image update if a new one is provided
        if form.image.data:
            post.image_file = save_post_thumbnail(form.image.data)

        db.session.commit()
        flash('Update modified successfully!', 'success')
        return redirect(url_for('project.project_details', project_id=post.project_id))

    # Pre-populate the form for the GET request
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.post_type.data = post.post_type
        

    return render_template('create_post.html', title='Edit Update', form=form, project=post.project)

@post_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def post_delete(post_id):
    post = Posts.query.get_or_404(post_id)
    project_id = post.project_id

    if post.user_id != current_user.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for('project.project_details', project_id=project_id))

    db.session.delete(post)
    db.session.commit()
    flash('Update deleted!', 'info')
    return redirect(url_for('project.project_details', project_id=project_id))