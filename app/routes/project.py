from flask import Blueprint , render_template , redirect , url_for , flash , request, jsonify, current_app
from flask_login import login_required , current_user
from app.form import ProjectForm
from app import db
from app.models import Projects , Posts
from app.routes.service import generate_project_reel
import threading

project_bp = Blueprint('project',__name__)


@project_bp.route('/project/new', methods=['GET', 'POST'])
@login_required
def new_project():

    form = ProjectForm()
    if form.validate_on_submit():
        project_exist = Projects.query.filter_by(title=form.title.data, user_id=current_user.id).first()
        if project_exist:
            flash('You already have a project with this name', 'danger')
            return render_template('new_project.html', form=form)

        new_project = Projects(
            title=form.title.data,
            description=form.description.data,
            status=form.status.data,
            start_date=form.start_date.data,
            user_id=current_user.id,
            tech_stack=form.tech_stack.data,
            repo_url=form.repo_url.data
        )
        db.session.add(new_project)
        db.session.commit()
        
        flash('New Project Created!', 'success')
        return redirect(url_for('project.view_projects')) # Must match function name below
    
    return render_template('new_project.html', form=form)

@project_bp.route('/project', methods=["GET"])
@login_required
def view_projects():
    user_projects  = Projects.query.filter_by(user_id=current_user.id).all()
    return render_template('projects.html', projects=user_projects)

@project_bp.route('/project/<int:project_id>',methods=['GET','POST'])
@login_required
def project_details(project_id):
    project = Projects.query.get_or_404(project_id)

    if project.user_id != current_user.id:
        flash("You do not have permission to view this project.", "danger")
        return redirect(url_for('project.view_projects'))

    # Check if reel exists
    import os
    reel_path = os.path.join('app', 'static', 'videos', f'project_{project_id}_reel.mp4')
    has_reel = os.path.exists(reel_path)
    reel_url = url_for('static', filename=f'videos/project_{project_id}_reel.mp4') if has_reel else None

    return render_template('project_detail.html', project=project, ai_script=None)

@project_bp.route('/project/<int:project_id>/edit',methods=['GET','POST'])
@login_required
def project_edit(project_id):
    project = Projects.query.get_or_404(project_id)

    if project.user_id != current_user.id:
        flash("You can only edit your own projects!", "danger")
        return redirect(url_for('project.view_projects'))
    
    form = ProjectForm()

    if form.validate_on_submit():
        project.title = form.title.data
        project.description = form.description.data
        project.status = form.status.data
        project.start_date = form.start_date.data
        project.tech_stack = form.tech_stack.data
        project.repo_url = form.repo_url.data
        
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('project.project_details', project_id=project.id))
    
    elif request.method == 'GET':
        form.title.data = project.title
        form.description.data = project.description
        form.status.data = project.status
        form.start_date.data = project.start_date
        form.tech_stack.data = project.tech_stack
        form.repo_url.data = project.repo_url

    return render_template('edit_project.html',form=form , project=project)

@project_bp.route('/project/<int:project_id>/delete', methods=['POST']) 
@login_required
def project_delete(project_id):
    project = Projects.query.get_or_404(project_id) 
    
    if project.user_id != current_user.id:
        flash("You are not authorized to delete this project!", "danger")
        return redirect(url_for('project.view_projects'))
    
    db.session.delete(project)
    db.session.commit()
    
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('project.view_projects'))

@project_bp.route('/project/<int:project_id>/generate-reel', methods=['POST'])
@login_required
def generate_reel(project_id):
    """Generate AI reel for a project."""
    project = Projects.query.get_or_404(project_id)
    
    if project.user_id != current_user.id:
        flash("You do not have permission to generate a reel for this project.", "danger")
        return redirect(url_for('project.project_details', project_id=project_id))
    
    # Check if project has posts
    if not project.posts:
        flash('Please add at least one update to generate a reel.', 'warning')
        return redirect(url_for('project.project_details', project_id=project_id))
    
    # Run generation in background thread
    def generate_in_background(app_context):
        with app_context:
            try:
                print(f"[REEL] Starting generation for project {project_id}")
                video_path = generate_project_reel(project_id)
                if video_path:
                    print(f"[REEL] Successfully generated: {video_path}")
                else:
                    print(f"[REEL] Failed to generate reel for project {project_id}")
            except Exception as e:
                import traceback
                print(f"[REEL] Error generating reel: {e}")
                print(traceback.format_exc())
    
    # Get Flask app context to pass to thread
    app_context = current_app.app_context()
    app_context.push()
    
    thread = threading.Thread(target=generate_in_background, args=(app_context,))
    thread.daemon = True
    thread.start()
    
    flash('Reel generation started! This may take a few minutes. Please refresh the page to see the result.', 'info')
    return redirect(url_for('project.project_details', project_id=project_id))

@project_bp.route('/project/<int:project_id>/generate')
@login_required
def generate_ai_script(project_id):
    pass
