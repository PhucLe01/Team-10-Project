from app import myapp_obj
from app.forms import LoginForm, SignUpForm
from flask import render_template, flash, redirect

from app import db
from app.models import User, Post
from flask_login import current_user, login_user, logout_user, login_required

@myapp_obj.route("/")
def begin():
    return redirect("/login")

@myapp_obj.route("/logout")
def logout():
    logout_user()
    return redirect('/login')

@myapp_obj.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Login invalid username or password!')
            return redirect('/login')
        login_user(user)
        flash(f'Login requested for user {form.username.data}')
        flash(f'Login password {form.password.data}')
        return redirect('/home')
    return render_template("login.html", title = 'Sign in', form=form)

@myapp_obj.route('/signup', methods = ['GET', 'POST'])
def SignUp():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is None:
            new_user = User(username = form.username.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash(f'The user {form.username.data} is created')
            return redirect('/login')
        elif user is not None:
            flash(f'The user {form.username.data} already exist.')
    return render_template('signup.html', title = 'Sign up', form = form)

@myapp_obj.route("/home")
def home():
    return render_template('home.html')