from app import myapp_obj
from datetime import datetime
import time
from app.forms import LoginForm, SignUpForm, flashCardForm, FlashShareForm, TaskForm
from flask import render_template, flash, redirect

from app import db
from app.models import User, FlashCard, Task
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
        flash(f'Login as {form.username.data}')
        return redirect(f'/home/{user.id}')
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

@myapp_obj.route("/home/<int:id>")
def home(id):
    posts = []
    allCards = FlashCard.query.filter_by(User = id).all()

    for x in range(len(allCards)): #sorting algorithm from GeeksforGeeks
        minRank = x
        for y in range(x+1, len(allCards)):
            if allCards[minRank].wrongguesscount < allCards[y].wrongguesscount:
                minRank = y     
        allCards[x], allCards[minRank] = allCards[minRank], allCards[x]

    uid = id
    if allCards is not None:
        for flashc in allCards:
            posts = posts + [
                {
                    'Label':f'{flashc.label}',
                    'Description':f'{flashc.description}',
                    'id':f'{flashc.id}',
                    'wrongcount':f'{flashc.wrongguesscount}'
                }
            ]
    return render_template('home.html', title = 'Flashcards', cardlist = posts, uid = uid)


@myapp_obj.route("/createcard/<int:id>", methods = ['GET', 'POST'])
def createcard(id):
    form = flashCardForm()
    if form.validate_on_submit():
        newCard = FlashCard(label = form.cardname.data, description = form.description.data, wrongguesscount = 0)
        newCard.set_user(id)
        db.session.add(newCard)
        db.session.commit()
        flash('New flashcard created')
        return redirect(f'/home/{id}')
    return render_template('createflashcard.html', title = 'Create flashcard', form = form, uid = id)

@myapp_obj.route("/description/<int:uid>/<int:id>", methods = ['GET', 'POST'])
def description(uid, id):
    flashcard = FlashCard.query.filter_by(id = id).first()
    description = flashcard.description
    return render_template('description.html', title = 'Card Description', description = description, uid = uid, id = id)

@myapp_obj.route("/deleteaccount/<int:uid>", methods = ['GET', 'POST'])
def deleteAccount(uid):
    target = User.query.filter_by(id = uid).first()
    name = target.username
    db.session.delete(target)
    db.session.commit()
    flash(f'User {name} has been deleted')
    return redirect('/login')

@myapp_obj.route("/incwrongcount/<int:uid>/<int:id>", methods = ['GET', 'POST'])
def incwrongcount(uid, id):
    flashcard = FlashCard.query.filter_by(id = uid).first()
    flashcard.inc_wrong_count()
    db.session.commit()
    return redirect(f'/home/{uid}')

@myapp_obj.route("/decwrongcount/<int:uid>/<int:id>", methods = ['GET', 'POST'])
def decwrongcount(uid, id):
    flashcard = FlashCard.query.filter_by(id = id).first()
    flashcard.dec_wrong_count()
    db.session.commit()
    return redirect(f'/home/{uid}')

@myapp_obj.route("/shareflashcard/<int:uid>/<int:id>", methods = ['GET', 'POST'])
def shareflashcard(uid, id):
    form = FlashShareForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.name.data).first()
        if user is None:
            flash('User does not exist')
        elif user.id is uid:
            flash('Cannot share with yourself')
        else:
            card = FlashCard.query.filter_by(id = id).first()
            newCard = FlashCard(label = card.label, description = card.description, wrongguesscount = 0)
            newCard.set_user(user.id)
            db.session.add(newCard)
            db.session.commit()
            return redirect(f'/home/{uid}')
    return render_template('shareflashcard.html', title = 'Share flashcard with another user', form = form, uid = uid)

@myapp_obj.route("/taskviewer/<int:uid>")
def taskviewer(uid):
    posts = []
    alltasks = Task.query.filter_by(User = uid).all()

    # uid = id
    if alltasks is not None:
        for task in alltasks:
            posts = posts + [
                {
                    'Name':f'{task.label}',
                    'Start_date':f'{task.startdate.strftime("%m/%d/%Y")}',
                    'id':f'{task.id}',
                    'Deadline':f'{task.deadline.strftime("%m/%d/%Y")}',
                    'Status':f'{task.status}'
                }
            ]
    return render_template('taskview.html', title = 'Task viewer', alltasks = posts, uid = uid)

@myapp_obj.route("/createtask/<int:uid>", methods = ['GET', 'POST'])
def createtask(uid):
    form = TaskForm()
    if form.validate_on_submit():
        try:
            newtask = Task(label = form.name.data)
            newtask.set_startdate(form.startdate.data)
            newtask.set_deadline(form.deadline.data)
            newtask.set_user(uid)
            db.session.add(newtask)
            db.session.commit()
            flash('New task added')
            return redirect(f'/taskviewer/{uid}')
        except:
            flash('Invalid input')
    return render_template('createtask.html', title = 'Create task', form = form, uid = uid)

@myapp_obj.route("/finishtask/<int:uid>/<int:id>", methods = ['GET', 'POST'])
def finishtask(uid, id):
    task = Task.query.filter_by(id = id).first()
    task.set_status()
    db.session.commit()
    return redirect(f'/taskviewer/{uid}')

@myapp_obj.route("/pomodorostudy/<int:uid>/<int:t>", methods = ['GET', 'POST'])
def study(uid, t):
    if t > 0:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        t -= 5
        time.sleep(5)
        #change to javascript so we can redirect inside the html
        return redirect(f'/pomodorostudy/{uid}/{t}')
        
    else:
        timer = '00:00'
    return render_template('pomodorostudy.html', title = 'Study time', timer = timer, uid = uid)
