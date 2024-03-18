import enum

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from enum import Enum



user_project=db.Table('user_project',
                      db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
                      db.Column('project_id',db.Integer,db.ForeignKey('project.id')))
user_task=db.Table('user_task',
                   db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
                   db.Column('task_id',db.Integer,db.ForeignKey('task.id')))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    projects = db.relationship('Project',secondary=user_project, backref='users')
    tasks=db.relationship('Task',secondary=user_task, backref='users')
    experience=db.Column(db.String(), nullable=False)
    type = db.Column(db.String(), nullable=False)
    notifications = db.relationship('Notification', backref='user')
    photo = db.Column(db.String(10000))


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type=db.Column(db.String(10000))
    message = db.Column(db.String(10000))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10000))
    description = db.Column(db.String(10000))
    end_date = db.Column(db.DateTime(timezone=True))
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sections=db.relationship('Section',backref='project')
    progress = db.Column(db.Integer)
    github = db.Column(db.String(100))


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    tasks = db.relationship('Task',backref='section')


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10000))
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    description = db.Column(db.String(10000))
    status = db.Column(db.String(10000))
    priority = db.Column(db.String(10000))
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    comments = db.relationship('Comment',backref='chat')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
    content = db.Column(db.String(10000))
    creation_date = db.Column(db.DateTime(timezone=True))

