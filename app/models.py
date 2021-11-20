from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin
from app import login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password  = db.Column(db.String(128))
    card = db.relationship('FlashCard', backref = 'Users')

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

    def set_user(self, id):
        self.User = id

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
