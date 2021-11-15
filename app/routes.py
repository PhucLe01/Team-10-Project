from app import myapp_obj
from app.forms import LoginForm
from flask import render_template, flash, redirect

from app import db
from app.models import User, Post
from flask_login import current_user, login_user, logout_user, login_required

@myapp_obj.route("/loggedin")
@login_required
def log():
    return 'Hi you are logged in'

@myapp_obj.route("/logout")
def logout():
    logout_user()
    return redirect('/')

@myapp_obj.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Login invalid username or password!')
            return redirect('/login')
        login_user(user, remember=form.remember_me.data)
        flash(f'Login requested for user {form.username.data},remember_me={form.remember_me.data}')
        flash(f'Login password {form.password.data}')
        return redirect('/')
    return render_template("login.html", form=form)

@myapp_obj.route("/members/<string:name>/")
def getMember(name):
    return 'Hi ' + name

@myapp_obj.route("/")
def home():
    name = 'Thomas'
    people = {'Carlos' : 54}
    title = 'My HommePage'
    posts = [{'author': 'john', 'body': 'Beautiful day in Portland!'},\
            {'author': 'Susan', 'body': 'Today was a good day!'}]

    return render_template('home.html', name=name, people=people, posts=posts)
