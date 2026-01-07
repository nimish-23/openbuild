from flask import Blueprint , render_template , redirect , url_for , flash , request, jsonify, current_app
from flask_login import login_required , current_user
from app.form import ProjectForm
from app import db
from app.models import Projects , Posts
from app.ai.summary import generate_ai_summary
from export import export_project_data
from datetime import datetime

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


@project_bp.route('/project/<int:project_id>/ai-summary', methods=['GET'])
@login_required
def ai_summary(project_id):
    project = Projects.query.get_or_404(project_id)

    if project.user_id != current_user.id:
        flash("You do not have permission to view this project.", "danger")
        return redirect(url_for('project.view_projects'))

    return render_template(
        'ai_summary.html',
        project=project
    )


@project_bp.route('/project/<int:project_id>/ai-summary/generate', methods=['POST'])
@login_required
def ai_summary_generate_ready(project_id):
    project = Projects.query.get_or_404(project_id)

    if project.user_id != current_user.id:
        flash("You do not have permission to view this project.", "danger")
        return redirect(url_for('project.view_projects'))

    project_json = export_project_data(project_id)
    summary_text = generate_ai_summary(project_json)
    
    if not summary_text:
        flash('Failed to generate AI summary.', 'danger')
        return redirect(url_for('project.ai_summary', project_id=project.id))

    project.ai_summary = summary_text
    project.ai_summary_version = "1.1.0"
    project.ai_summary_generated_at = datetime.now()
    db.session.commit()

    flash('AI summary generated successfully!', 'success')
    return redirect(url_for('project.ai_summary', project_id=project.id))


    