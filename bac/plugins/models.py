from datetime import datetime
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
import click
from enum import IntFlag, auto,IntEnum

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

class Theme(IntFlag):
    ANTIBIOGRAM = auto()
    DIRECT_EXAM = auto()
    CULTURE = auto()
    OTHER = auto()

    def all():
        return Theme.ANTIBIOGRAM | Theme.DIRECT_EXAM | Theme.CULTURE | Theme.OTHER
    
class Job(IntEnum):
    STUDENT = auto()
    TECH = auto()
    BIOLOGIST = auto()
    INTERN = auto()
    ADMIN = auto()
    OTHER = auto()
    
class User(UserMixin,db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,primary_key=True)
    firstname = db.Column(db.String,nullable=False)
    name = db.Column(db.String,nullable=False)  
    email = db.Column(db.String,unique=True,nullable=False)
    theme = db.Column(db.Integer,nullable=False,default= Theme.all())
    job = db.Column(db.Integer,nullable=False,default = Job.OTHER)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)

    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    last_connection = db.Column(db.DateTime,nullable=True)

    def __init__(
            self, 
            firstname,
            name,
            email, 
            password,
            job = Job.OTHER,
            is_admin=False,
            is_confirmed=False,
            confirmed_on=None
        ):        
            self.firstname = firstname
            self.name = name
            self.email = email
            self.password = bcrypt.generate_password_hash(password)
            self.job = job
            self.created_on = datetime.now()
            self.is_admin = is_admin
            self.is_confirmed = is_confirmed
            self.confirmed_on = confirmed_on
            self.last_connection = datetime.now()

    def __repr__(self):
        return f"<email {self.email}>"
  
class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String,nullable=False)
    body = db.Column(db.String)
    legend = db.Column(db.String)
    created_on = db.Column(db.DateTime, nullable=False)
    theme = db.Column(db.Integer,nullable=False,default=Theme.all())
    level = db.Column(db.Integer,nullable=False,default=0)

class Answer(db.Model):
    __tablename__ = "answers"

    id = db.Column(db.Integer,primary_key=True)
    question_id = db.Column(db.Integer,nullable=False)
    title = db.Column(db.String,nullable=False)
    body = db.Column(db.String)
    solution = db.Column(db.Boolean, nullable=False, default=False)

class Image(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer,primary_key=True)
    question_id = db.Column(db.Integer,nullable=False)
    path = db.Column(db.String,nullable=False)  


class Session(db.Model):
    __tablename__ = "session"

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    size = db.Column(db.Integer)
    score = db.Column(db.Integer)

@click.command("load-file")
@click.argument('path',nargs=-1)
def load_questions(path):
    click.echo(f'Load csv file {path}')
    # TODO