from flask import Blueprint , render_template , redirect , url_for , flash
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