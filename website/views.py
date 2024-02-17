from datetime import datetime

from flask import render_template, request, redirect, url_for, flash, Blueprint, jsonify
from flask_login import login_required, current_user
from .models import Project, User, Section
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        # checking if this is the project creation form
        if 'name' in request.form and 'description' in request.form and 'end_date' in request.form:
            name = request.form.get('name')
            description = request.form.get('description')
            date = request.form.get('end_date')
            end_date=datetime.strptime(date, '%Y-%m-%d').date()
            if len(name) < 1:
                flash('Project name is too short.', category='error')
            else:
                flash('Project added', category='success')
                new_project = Project(name=name, admin_id=current_user.id, description=description, end_date=end_date, sections=[])
                db.session.add(new_project)
                current_user.projects.append(new_project)
                db.session.commit()
                return redirect(url_for('views.home'))
                # otherwise it's the project renaming form
        else:
            name = request.form.get('name1')
            project_id = request.form.get('project_id')
            if len(name) < 1:
                flash('Project is too short.', category='error')
            else:
                flash('Project renamed', category='success')
                old_project = Project.query.get(project_id)
                new_project = Project()  # Create a new instance of the Project model
                new_project.name = name  # Assign the new name to the new project
                # Copy other attributes as needed
                new_project.id = old_project.id
                new_project.admin_id = old_project.admin_id
                new_project.end_date = old_project.end_date
                new_project.description = old_project.description
                new_project.sections = []
                for section in old_project.sections:
                    new_project.sections.append(section)
                if old_project in current_user.projects:
                    current_user.projects.remove(old_project)
                # Remove the old project from the session and delete it from the database
                db.session.delete(old_project)
                # Update the relationships with the new project
                current_user.projects.append(new_project)
                # Add the new project to the session and commit the changes
                db.session.add(new_project)
                db.session.commit()
                return redirect(url_for('views.home'))

    return render_template("home.html",user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file
    noteId = note['noteId']
    note = Project.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

@views.route('/delete-project', methods=['POST'])
def delete_project():
    project = json.loads(request.data) # this function expects a JSON from the INDEX.js file
    projectId = project['projectId']
    project = Project.query.get(projectId)
    if project:
        if project.admin_id == current_user.id:
            db.session.delete(project)
            db.session.commit()
    return jsonify({})

@views.route('/project/<project_id>', methods=['GET', 'POST'])
def project(project_id):
    project = Project.query.get(project_id)
    if request.method == 'POST':
        name = request.form.get('name')
        if len(name) < 1:
            flash('Section name is too short.', category='error')
        else:
            flash('Section added', category='success')
            new_section = Section(name=name, project_id=project_id)
            db.session.add(new_section)
            project.sections.append(new_section)
            db.session.commit()
           # return redirect(url_for('project/' + project_id))
    # Here you would fetch the project data corresponding to project_id
    # For example, if you have a database, you would query the database for the project details

    # Assuming you have the project data available, you would pass it to the template


    return render_template('project.html', user=current_user, project=project)

@views.route('/delete-section', methods=['POST'])
def delete_section():
    section = json.loads(request.data) # this function expects a JSON from the INDEX.js file
    sectionId = section['sectionId']
    section = Section.query.get(sectionId)
    if section:
        db.session.delete(section)
        db.session.commit()
    return jsonify({})