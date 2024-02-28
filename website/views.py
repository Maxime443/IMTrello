from datetime import datetime

from flask import render_template, request, redirect, url_for, flash, Blueprint, jsonify
from flask_login import login_required, current_user
from .models import Project, User, Section, Task
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
                new_project = Project(name="Project " + name, admin_id=current_user.id, description=description, end_date=end_date, sections=[])
                db.session.add(new_project)
                current_user.projects.append(new_project)
                db.session.commit()
                return redirect(url_for('views.home'))
                # otherwise it's the project renaming form
        else:
            name = request.form.get('name4')
            project_id = request.form.get('project_id')
            if len(name) < 1:
                flash('Project is too short.', category='error')
            else:
                flash('Project renamed', category='success')
                old_project = Project.query.get(project_id)
                old_project.name = name
                db.session.commit()
                return redirect(url_for('views.home'))

    return render_template("home.html",user=current_user)

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
    developers = User.query.filter_by(type='DEVELOPER').all()  # Récupérer tous les utilisateurs depuis la base de données
    user_emails = [user.email for user in developers]  # Extraire les adresses e-mail des utilisateurs
    user_task_records = developers
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add_section':
            name = request.form.get('section_name')
            new_section = Section(name="Section " + name, project_id=project_id, tasks=[])
            db.session.add(new_section)
            project.sections.append(new_section)
            db.session.commit()

        elif action == "add_developer":
            selected_emails = request.form.getlist('developer_emails')  # Récupérer les adresses e-mail sélectionnées
            print(selected_emails)
            devs = User.query.filter(User.email.in_(selected_emails)).all()  # Sélectionner les utilisateurs correspondant aux adresses e-mail sélectionnées
            for developer in devs:
                developer.projects.append(Project.query.get(project_id))
            db.session.commit()
            return render_template('project.html', user=current_user, project=project,user_emails=user_emails,
                                   user_task_records=user_task_records)

        elif action == 'add_task':
            name = request.form.get('task_name')
            section_id = request.form.get('task_section_id')
            print(section_id)
            description = request.form.get('task_description')
            new_task = Task(name="Task " + name, section_id=section_id, description=description, status='uncompleted', priority='medium')
            db.session.add(new_task)
            section = Section.query.get(section_id)
            section.tasks.append(new_task)
            db.session.commit()

        elif action == "add_developer_to_task":
            # Récupérer les adresses e-mail sélectionnées
            task_id = request.form.get('task_id')

            selected_emails = request.form.getlist('developer_emails_for_task')
            task = Task.query.get(task_id)
            if task:
                flash('task found with id : ' + task_id, category='success')

            devs = User.query.filter(User.email.in_(
                selected_emails)).all()

            # Sélectionner les utilisateurs correspondant aux adresses e-mail sélectionnées
            x = 0
            dess = ""
            for developer in devs:
                if task not in developer.tasks:
                    x += 1
                    developer.tasks.append(task)
                else:
                    dess += developer.first_name + " "
                    x -= 1
            y = str(x)


            db.session.commit()
            return render_template('project.html', user=current_user, project=project, user_emails=user_emails,
                                   user_task_records=user_task_records)

        else:
            return render_template('project.html', user=current_user, project=project,user_emails=user_emails,
                           user_task_records=user_task_records)
    return render_template('project.html', user=current_user, project=project,user_emails=user_emails,
                           user_task_records=user_task_records)

@views.route('/delete-section', methods=['POST'])
def delete_section():
    section = json.loads(request.data) # this function expects a JSON from the INDEX.js file
    sectionId = section['sectionId']
    section = Section.query.get(sectionId)
    if section:
        db.session.delete(section)
        db.session.commit()
    return jsonify({})


@views.route('/delete-task', methods=['POST'])
def delete_task():
    res = json.loads(request.data) # this function expects a JSON from the INDEX.js file

    taskId = res['taskId']

    task = Task.query.get(taskId)
    if task:
        db.session.delete(task)
        db.session.commit()
    return jsonify({})


@views.route('/remove-dev', methods=['POST'])
def remove_dev():
    res = json.loads(request.data)  # Use request.get_json() to parse JSON data
    task_id = res['task_id']  # Access task_id from the JSON data
    user_id = res['user_id']  # Access user from the JSON data

    # Assuming db is the SQLAlchemy database object
    task = Task.query.get(task_id)
    user = User.query.get(user_id)
    if task in user.tasks:
        # Assuming db is the SQLAlchemy database object
        user.tasks.remove(task)  # Use remove() to remove task from user's tasks
        db.session.commit()
    return jsonify({})


@views.route('/get-task-infos/<int:task_id>', methods=['GET'])
def get_task(task_id):
    flash('Task added', category='success')
    task = Task.query.get(task_id)
    if task:
        return jsonify({'id': task.id, 'name': task.name, 'description': task.description,
                        'status': task.status})  # Return the task details
    else:
        return jsonify({'error': 'Task not found'}), 404  # Return an error if the task is not found


@views.route('/update_task_status/<int:task_id>', methods=['POST'])
def update_task_status(task_id):
    task = Task.query.get(task_id)
    if not task:
        return 'Task not found.', 404
    if request.method == 'POST':
        new_status = request.json.get('status')
        if not new_status:
            return 'New task status not provided.', 400
        # Update task status
        task.status = new_status
        db.session.commit()
        return 'Task status updated successfully.', 200

@views.route('/update_task_priority/<int:task_id>', methods=['POST'])
def update_task_priority(task_id):
    task = Task.query.get(task_id)
    if not task:
        return 'Task not found.', 404
    if request.method == 'POST':
        new_priority = request.json.get('priority')
        if not new_priority:
            return 'New task priority not provided.', 400
        # Update task status
        task.priority = new_priority
        db.session.commit()
        return 'Task priority updated successfully.', 200


