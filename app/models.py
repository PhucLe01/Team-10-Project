from app import db
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin
from app import login


class User(UserMixin, db.Model):
    '''
    The user database

    This keep track of the user's id, username, password, their flashcards, tasks, and notes
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128))
    card = db.relationship('FlashCard', backref = 'Users')
    task = db.relationship('Task', backref = 'Users')
    note = db.relationship('Note', backref = 'Users')

    def set_password(self, password):
        '''
        Set the password

        This fuction set the password of the user after hashing the given value

        Parameters
        -------
        password : String
            input to be use as the password

        '''
        self.password = generate_password_hash(password)

    def check_password(self, password):
        '''
        Check the password

        This function compare the given password with the password of the user

        Parameter
        -------
        password : String
            The string to be compared to the user's password

        return
        -------
        boolean
            True or flase if the two string match
        '''
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.id}: {self.username}>'

class FlashCard(db.Model):
    '''
    The flashcard database

    This keep track of the flashcard's id, label, description, wrong guess count, and the id of the user it belongs to
    '''
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String)
    description = db.Column(db.String)
    wrongguesscount = db.Column(db.Integer)
    User = db.Column(db.Integer, db.ForeignKey('user.id'))

    def set_user(self, uid):
        '''
        set the user of this flashcard

        Parameter
        -------
        uid : int
            The id of the user
        '''
        self.User = uid

    def inc_wrong_count(self):
        '''
        Increase wrongguesscount by 1

        This function will increment the wrongguesscount counter of the flashcard by 1
        '''
        self.wrongguesscount = self.wrongguesscount + 1

    def dec_wrong_count(self):
        '''
        Decrease wrongguesscount by 1

        This function will decrement the wrongguesscount counter of the flashcard by 1
        '''
        if self.wrongguesscount > 0:
            self.wrongguesscount = self.wrongguesscount - 1

class Task(db.Model):
    '''
    The task database

    This keep track of the task's id, label, startdate, dealine, complete status, and the id of the user it belongs to
    '''
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String)
    startdate = db.Column(db.DateTime, index=True, unique = False)
    deadline = db.Column(db.DateTime, index=True, unique = False)
    status = db.Column(db.Boolean, default=False)
    User = db.Column(db.Integer, db.ForeignKey('user.id'))

    def set_user(self, uid):
        '''
        set the user of this task

        Parameter
        -------
        uid : int
            The id of the user
        '''
        self.User = uid

    def set_startdate(self, startdate):
        '''
        set the startdate of this task

        Parameter
        -------
        startdate : date and time
            The start date for this task
        '''
        self.startdate = datetime.strptime(startdate, '%m/%d/%Y')

    def set_deadline(self, deadline):
        '''
        set the dealine of this task

        Parameter
        -------
        deadline : date and time
            The end date for this task
        '''
        self.deadline = datetime.strptime(deadline, '%m/%d/%Y')

    def set_status(self):
        '''
        Set status of the task to true
        '''
        self.status = True
        
class Note(db.Model):
    '''
    The note database

    This keep track of the note's id, name, file data, and the user id it belongs to
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    data = db.Column(db.LargeBinary)
    User = db.Column(db.Integer, db.ForeignKey('user.id'))

    def set_user(self, uid):
        '''
        set the user of this note

        Parameter
        -------
        uid : int
            The id of the user
        '''
        self.User = uid

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
