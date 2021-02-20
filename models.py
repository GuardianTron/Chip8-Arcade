from flask_sqlalchemy import SQLAlchemy
from flask_security.models import fsqla_v2 as fsqla
from sqlalchemy.orm import backref

db = SQLAlchemy()

roles_users = db.Table('roles_users',
    db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
    db.Column('role_id',db.Integer,db.ForeignKey('role.id'))
)

class User(db.Model,fsqla.FsUserMixin):

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255),unique=True, nullable=False)
    email = db.Column(db.String(255),unique=True,nullable=False)
    password = db.Column(db.Text(),nullable=False)
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role',secondary='roles_users',
                            backref=db.backref('users',lazy='dynamic'))

class Role(db.Model,fsqla.FsRoleMixin):
    id = db.Column(db.Integer,primary_key=True)
    role = db.Column(db.String(80),unique=True)
    description = db.Column(db.Text)

class Game(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    title = db.Column(db.String(255),nullable=False)
    description = db.Column(db.Text)
    filename = db.Column(db.String(255),nullable=False)
    user = db.relationship('User',backref=db.backref('games',lazy='dynamic'))