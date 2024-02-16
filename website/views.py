from datetime import datetime

from flask import render_template, request, redirect, url_for, flash, Blueprint, jsonify
from flask_login import login_required, current_user
from .models import Project, User
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        date = request.form.get('end_date')
        end_date=datetime.strptime(date, '%Y-%m-%d').date()
        if len(name) < 1:
            flash('Project is too short.', category='error')
        else:
            flash('Project added', category='success')
            new_project = Project(name=name, admin_id=current_user.id, description=description, end_date=end_date)
            db.session.add(new_project)
            current_user.projects.append(new_project)
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