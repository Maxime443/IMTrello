import enum

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from enum import Enum


class Type(Enum):
    PROJECT_MANAGER = 0
    DEVELOPER = 1

user_project=db.Table('user_project',
                      db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
                      db.Column('project_id',db.Integer,db.ForeignKey('project.id')))
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    projects = db.relationship('Project',secondary=user_project, backref='users')
    type = db.Column(db.Enum(Type), nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10000))
    #start_date=db.Column(db.DateTime(timezone=True), default=func.now())
    #end_date = db.Column(db.DateTime(timezone=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sections=db.relationship('Section',backref='project')
    def __init__(self, name, user_id, sections):
        self.name = name
        self.user_id = user_id
        self.sections = sections

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))