from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    '''
    This class contain the form for the login page
    '''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign in')

class SignUpForm(FlaskForm):
    '''
    This class contain the form for the sign up page
    '''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign up')

class flashCardForm(FlaskForm):
    '''
    This class contain the form for the flashcard creation page
    '''
    cardname = StringField('Card label', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    createcard = SubmitField('Create flash card')

class FlashShareForm(FlaskForm):
    '''
    This class contain the form for the share flashcard with other users page
    '''
    name = StringField('Username', validators=[DataRequired()])
    share = SubmitField('Share')

class TaskForm(FlaskForm):
    '''
    This class contain the form for the create task page
    '''
    name = StringField('Task', validators=[DataRequired()])
    startdate = StringField('Start date (mm/dd/yyyy)', validators = [DataRequired()])
    deadline = StringField('Deadline (mm/dd/yyyy)', validators = [DataRequired()])
    submit = SubmitField('submit')

class NoteForm(FlaskForm):
    '''
    This class contain the form for the upload markdown notes page
    '''
    name = StringField('name', validators={DataRequired()})
    note = FileField('file', validators={DataRequired()})
    submit = SubmitField('submit')