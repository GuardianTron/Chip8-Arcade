from flask_sqlalchemy import SQLAlchemy
from flask_security_too import UserMixin, RoleMixin

db = SQLAlchemy()

roles_users = db.Table('roles_users',
    db.Column('user_id',db.Integer(db.ForeignKey('user.id'))),
    db.Column('role_id',db.Integer(db.ForeignKey('role.id')))
)

class User(db.Model,UserMixin):

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255),unique=True, nullable=False)
    email = db.Column(db.String(255),unique=True,nullable=False)
    password = db.Column(db.Text(),nullable=False)
    active = db.Column(db.Boolean(default=True))
    confirmed_at = db.Column(db.DateTime())
    roles = db.Relationship('Roles',secondary='roles_users',
                            backref=db.backref('users',lazy='dynamic'))

class Role(db.Model,RoleMixin):
    id = db.Column(db.Integer,primary_key=True)
    role = db.Column(db.String(80),unique=True)
    description = db.Column(db.String)

