from abc import abstractmethod
from operator import attrgetter
from flask import current_app
from flask_sqlalchemy import SQLAlchemy,event
from flask_security.models import fsqla_v2 as fsqla
from sqlalchemy.orm import backref
from sqlalchemy.ext.hybrid import hybrid_property
import os
import uuid

db = SQLAlchemy()

roles_users = db.Table('roles_users',
    db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
    db.Column('role_id',db.Integer,db.ForeignKey('role.id'))
)

class FileSaveMixin:
    file = None
    #used for deleting old files when a new file is uploaded
    old_path = None
    
    @property
    def path(self):
        #make sure directory exists and make one if it doesn't
        #attempt to get per class configuration
        classname = self.__class__.__name__.lower()
        basedir = os.path.join(current_app.config['UPLOAD_FOLDER'],classname)
        if not hasattr(self,'_path'):

            #attempt to create directory if it does not exit
            if not os.path.isdir(basedir):
                os.mkdir(basedir)
        #make sure that setting filename changes path
        self._path = os.path.join(basedir,str(self.filename))
        return self._path

    @abstractmethod
    def save(self):
        pass


'''
Generates a unique filename whenever a new file is uploaded.
If update, saves old path for later deletion
'''
def generate_filename(mapper,connection,target):
    if target.file is not None:
        #save path for later deletion
        if target.filename is not None:
            target.old_path = target.path
        target.filename = uuid.uuid4().hex

event.listen(FileSaveMixin,'before_insert',generate_filename,propagate=True)
event.listen(FileSaveMixin,'before_update',generate_filename,propagate=True)



'''
Save new file if one has been uploaded.
Delete old file during update if one exists
'''        
def save_file(mapper,connection,target):
    if target.file is not None:    
        target.save()
        if target.old_path is not None and os.path.exists(target.old_path):
           os.remove(target.old_path)
           target.old_path=None


event.listen(FileSaveMixin,'after_insert',save_file,propagate=True)
event.listen(FileSaveMixin,'after_update',save_file,propagate=True)

@event.listens_for(FileSaveMixin,'after_delete',propagate=True)
def delete_file(mapper,connection,target):
    if target.path and os.path.exists(target.path):
        os.remove(target.path)

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

class Game(db.Model,FileSaveMixin):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    title = db.Column(db.String(255),nullable=False)
    description = db.Column(db.Text)
    filename = db.Column(db.String(255),nullable=False)
    user = db.relationship('User',backref=db.backref('games',lazy='dynamic'))

    def save(self):
        hex = self.file.hex()
        with open(self.path,'w') as writer:
            writer.write(hex)

    





        
