from app import db
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin
from app import login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128))
    card = db.relationship('FlashCard', backref = 'Users')
    task = db.relationship('Task', backref = 'Users')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.id}: {self.username}>'

class FlashCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String)
    description = db.Column(db.String)
    wrongguesscount = db.Column(db.Integer)
    User = db.Column(db.Integer, db.ForeignKey('user.id'))

    def set_user(self, uid):
        self.User = uid

    def inc_wrong_count(self):
        self.wrongguesscount = self.wrongguesscount + 1

    def dec_wrong_count(self):
        if self.wrongguesscount > 0:
            self.wrongguesscount = self.wrongguesscount - 1

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String)
    startdate = db.Column(db.DateTime, index=True, unique = False)
    deadline = db.Column(db.DateTime, index=True, unique = False)
    status = db.Column(db.Boolean, default=False)
    User = db.Column(db.Integer, db.ForeignKey('user.id'))

    def set_user(self, uid):
        self.User = uid

    def set_startdate(self, startdate):
        self.startdate = datetime.strptime(startdate, '%m/%d/%Y')

    def set_deadline(self, deadline):
        self.deadline = datetime.strptime(deadline, '%m/%d/%Y')

    def set_status(self):
        self.status = True

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
