from flask import Blueprint , render_template , redirect , url_for , flash , request
from flask_login import login_required , current_user
from app.form import ProjectForm
from app import db
from app.models import Projects

project_bp = Blueprint('project',__name__)


@project_bp.route('/project/new', methods=['GET', 'POST'])
@login_required
def new_project():
    # REMOVED: if current_user.is_authenticated check (it causes infinite redirect)
    
    form = ProjectForm()
    if form.validate_on_submit():
        # Phase 2: Check for duplicates (Optional but good)
        project_exist = Projects.query.filter_by(title=form.title.data, user_id=current_user.id).first()
        if project_exist:
            flash('You already have a project with this name', 'danger')
            return render_template('new_project.html', form=form)

        new_project = Projects(
            title=form.title.data,
            description=form.description.data,
            status=form.status.data,
            start_date=form.start_date.data,
            user_id=current_user.id
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

@project_bp.route('/project/<int:id>',methods=['GET','POST'])
def project_details(id):
    project = Projects.query.get_or_404(id)

    if project.user_id != current_user.id:
        flash("You do not have permission to view this project.", "danger")
        return redirect(url_for('project.view_projects'))

    return render_template('project_detail.html',project=project)

@project_bp.route('/project/<int:id>/edit',methods=['GET','POST'])
@login_required
def project_edit(id):
    project = Projects.query.get_or_404(id)

    if project.user_id != current_user.id:
        flash("You can only edit your own projects!", "danger")
        return redirect(url_for('project.view_projects'))
    
    form = ProjectForm()

    if form.validate_on_submit():
        project.title = form.title.data
        project.description = form.description.data
        project.status = form.status.data
        project.start_date = form.start_date.data
        # Add tech_stack/repo_url here if added to form
        
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('project.project_details', id=project.id))
    
    elif request.method == 'GET':
        form.title.data = project.title
        form.description.data = project.description
        form.status.data = project.status
        form.start_date.data = project.start_date

    return render_template('edit_project.html',form=form , project=project)

@project_bp.route('/project/<int:id>/delete', methods=['POST']) 
@login_required
def project_delete(id):
    project = Projects.query.get_or_404(id) 
    
    if project.user_id != current_user.id:
        flash("You are not authorized to delete this project!", "danger")
        return redirect(url_for('project.view_projects'))
    
    db.session.delete(project)
    db.session.commit()
    
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('project.view_projects'))