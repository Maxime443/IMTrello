import enum

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from enum import Enum


class Type(Enum):
    PROJECT_MANAGER=0
    DEVELOPER = 1

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    note = db.relationship('Note', backref='')
    type = db.Column(db.Enum(Type), nullable=False)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date=db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))