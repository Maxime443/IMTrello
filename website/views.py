from datetime import datetime

from flask import render_template, request, redirect, url_for, flash, Blueprint, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        text = request.form.get('note')
        if len(text) < 1:
            flash('Note is too short.', category='error')
        else:
            flash('Note added', category='success')
            new_note = Note(data=text, user_id=current_user.id,date=datetime.now())
            db.session.add(new_note)
            db.session.commit()
            return redirect(url_for('views.home'))
    return render_template("home.html",user=current_user)

@views.route('/home2', methods=['GET', 'POST'])
@login_required
def home2():
    if request.method == 'POST':
        text = request.form.get('note')
        if len(text) < 1:
            flash('Note is too short.', category='error')
        else:
            flash('Note added', category='success')
            new_note = Note(data=text, user_id=current_user.id,date=datetime.now())
            db.session.add(new_note)
            db.session.commit()
            return redirect(url_for('views.home2'))
    return render_template("home2.html",user=current_user)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

@views.route('/change-note', methods=['GET', 'POST'])
@login_required
def change_note():
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})