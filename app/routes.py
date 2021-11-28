from app import myapp_obj
from datetime import datetime
import time
from app.forms import LoginForm, SignUpForm, flashCardForm, FlashShareForm, TaskForm, NoteForm, NoteShareForm
from flask import render_template, flash, redirect, make_response, send_file
import pdfkit
import pypandoc
from io import BytesIO
from app import db
from app.models import User, FlashCard, Task, Note
from flask_login import current_user, login_user, logout_user, login_required

@myapp_obj.route("/")
def begin():
    '''
    This start off the website

    This function will bring the user to the login page

    '''
    return redirect("/login")

@myapp_obj.route("/logout")
def logout():
    '''
    Log the user out

    This fucntion will log the user out of their account and redirect them to the login page
    '''
    logout_user()
    return redirect('/login')

@myapp_obj.route("/login", methods=['GET', 'POST'])
def login():
    '''
    Log the user in

    This fucntion will log the user into their account and bring them to the home page if the credentials are correct

        Returns:
            Redirect to itself 
            Or
            template to login.html
            Or
            redirect to route /home
    '''
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
    '''
    Create an ccount

    This fuction will create an account if the input username and password are valid
    '''
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

@myapp_obj.route("/home/<int:uid>")
def home(uid):
    '''
    The home page

    This function will bring the user to the home page where all their flashcard are listed in the order of their wrongguesscount

    Parameter
    -------
    uid : int
        The id of the user that is logged in
    '''
    posts = []
    allCards = FlashCard.query.filter_by(User = uid).all()

    for x in range(len(allCards)): #sorting algorithm from GeeksforGeeks
        minRank = x
        for y in range(x+1, len(allCards)):
            if allCards[minRank].wrongguesscount < allCards[y].wrongguesscount:
                minRank = y     
        allCards[x], allCards[minRank] = allCards[minRank], allCards[x]

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


@myapp_obj.route("/createcard/<int:uid>", methods = ['GET', 'POST'])
def createcard(uid):
    '''
    flashcard creation page

    This function bring the user to the flashcard creation page. A new flashcard will be created if the inputs are correct and  teh user is redirected to the homepage when done

    Parameter
    -------
    uid : int
        The id of the user that is logged in
    '''
    form = flashCardForm()
    if form.validate_on_submit():
        newCard = FlashCard(label = form.cardname.data, description = form.description.data, wrongguesscount = 0)
        newCard.set_user(uid)
        db.session.add(newCard)
        db.session.commit()
        flash('New flashcard created')
        return redirect(f'/home/{uid}')
    return render_template('createflashcard.html', title = 'Create flashcard', form = form, uid = uid)

@myapp_obj.route("/description/<int:uid>/<int:id>", methods = ['GET', 'POST'])
def description(uid, id):
    '''
    The description of the flashcard

    This fucntion bring the user to a page that contain the description of the selected flashcard

    Parameter
    -------
    uid : int
        The id of the user that is logged in
    id : int
        The id of the flashcard that the user is seeing the description of
    '''
    flashcard = FlashCard.query.filter_by(id = id).first()
    description = flashcard.description
    return render_template('description.html', title = 'Card Description', description = description, uid = uid, id = id)

@myapp_obj.route("/deleteaccount/<int:uid>", methods = ['GET', 'POST'])
def deleteAccount(uid):
    '''
    Delete the current account

    This function will delete the current account. It will redirect the user to the login page afterwards

    Parameter
    -------
    uid : int
        The id of the user that is logged in
    '''
    target = User.query.filter_by(id = uid).first()
    name = target.username
    db.session.delete(target)
    db.session.commit()
    flash(f'User {name} has been deleted')
    return redirect('/login')

@myapp_obj.route("/incwrongcount/<int:uid>/<int:id>", methods = ['GET', 'POST'])
def incwrongcount(uid, id):
    '''
    Increase the wrongguesscount 
    
    This function will increment the wrong guess count of the current flashcard by 1. It redirects the user to the homepage afterwards
    
    Parameter
    -------
    uid : int
        The id of the user that is logged in
    id : int
        The id of the currrent flashcard
    '''
    flashcard = FlashCard.query.filter_by(id = id).first()
    flashcard.inc_wrong_count()
    db.session.commit()
    return redirect(f'/home/{uid}')

@myapp_obj.route("/decwrongcount/<int:uid>/<int:id>", methods = ['GET', 'POST'])
def decwrongcount(uid, id):
    '''
    Decrease the wrongguesscount 
    
    This function will decrement the wrong guess count of the current flashcard by 1. It redirects the user to the homepage afterwards
    
    Parameter
    -------
    uid : int
        The id of the user that is logged in
    id : int
        The id of the currrent flashcard
    '''
    flashcard = FlashCard.query.filter_by(id = id).first()
    flashcard.dec_wrong_count()
    db.session.commit()
    return redirect(f'/home/{uid}')

@myapp_obj.route("/shareflashcard/<int:uid>/<int:id>", methods = ['GET', 'POST'])
def shareflashcard(uid, id):
    '''
    Share current flashcard to another user

    This function will add a copy of the current flashcard to the user whos name was inputed. It redirect the user to the homepage afterwards

    Parameter
    -------
    uid : int
        The id of the user that is logged in
    id : int
        The id of the currrent flashcard
    '''
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
    return render_template('shareflashcard.html', title = 'Share flashcard', form = form, uid = uid)

@myapp_obj.route("/taskviewer/<int:uid>")
def taskviewer(uid):
    '''
    View all of the user's task

    This fucntion bring the user to the task page where all of their task are listed

    Parameter
    -------
    uid : int
        The id of the user that is logged in
    '''
    posts = []
    alltasks = Task.query.filter_by(User = uid).all()

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
    '''
    Create a task for the current user

    This function will create a task for the current user if the inputed name and dates are valid. It redirect teh user to the task page when done

    Parameter
    -------
    uid : int
        The id of the user that is logged in
    '''
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
    '''
    Mark the task as complete

    This function will set the status of the selected task to complete

    Parameter
    -------
    uid : int
        The id of the user that is logged in
    id : int
        The id of the selected task
    '''
    task = Task.query.filter_by(id = id).first()
    task.set_status()
    db.session.commit()
    return redirect(f'/taskviewer/{uid}')

@myapp_obj.route("/pomodorostudy/<int:uid>/<int:t>", methods = ['GET', 'POST'])
def study(uid, t):
    '''
    25 minute timer

    This function will bring the user to the 25 minute timer page and start the countdown

    Parameter
    -------
    uid : int
        The id of the user that is logged in
    t : int
        The time left on the timer in seconds
    '''
    if t == 1500:
        timer = '25:00'
        t -= 5
        return render_template('pomodorostudy.html', title = 'Study time', timer = timer, uid = uid, t = t)
    if t >= 0:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        t -= 5
        time.sleep(5)
    return render_template('pomodorostudy.html', title = 'Study time', timer = timer, uid = uid, t = t)

@myapp_obj.route("/pomodorobreak/<int:uid>/<int:t>", methods = ['GET', 'POST'])
def breaktime(uid, t):
    '''
    5 minute timer

    This function will bring the user to the 5 minute timer page and start the countdown

    Parameter
    -------
    uid : int
        The id of the user that is logged in
    t : int
        The time left on the timer in seconds
    '''
    if t == 300:
        timer = '5:00'
        t -= 5
        return render_template('pomodorobreak.html', title = 'Break time', timer = timer, uid = uid, t = t)
    if t >= 0:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        t -= 5
        time.sleep(5)
    return render_template('pomodorobreak.html', title = 'Break time', timer = timer, uid = uid, t = t)

@myapp_obj.route("/note/<int:uid>")
def note(uid):
    '''
    View all fo the user's note files

    This fucntion bring the user to the note page where all of their notes are listed

    Parameter
    -------
    uid : int
        The id of the user that is logged in
    '''
    posts = []
    allnotes = Note.query.filter_by(User = uid).all()

    if allnotes is not None:
        for note in allnotes:
            posts = posts + [
                {
                    'Name':f'{note.name}',
                    'id':f'{note.id}'
                }
            ]
    return render_template('note.html', title = 'Notes', allnotes = posts, uid = uid)

@myapp_obj.route("/noteuploadpage/<int:uid>", methods = ['GET', 'POST'])
def noteuploadpage(uid):
    '''
    Upload file

    This fucntion bring the user to the upload file page and will save the uploaded note file to the current user's account

    Parameter
    -------
    uid : int
        The id of the user that is logged in
    '''
    form = NoteForm()
    if form.validate_on_submit():
        newnote = Note(name = form.name.data, data = form.note.data.read())
        newnote.set_user(uid)
        db.session.add(newnote)
        db.session.commit()
    return render_template('uploadnote.html', title = 'Upload', form = form, uid = uid)

@myapp_obj.route("/viewnote/<int:uid>/<int:id>", methods = ['GET', 'POST'])
def viewnote(uid, id):
    '''
    (half working)
    View the content of the note

    This function bring the user to the viewnotes page where the contents of the selected note will be rendered

    Parameter
    -------
    uid : int
        The id of the user that is logged in
    id : int
        The id of the currrent note
    '''
    note = Note.query.filter_by(id = id).first()
    content = BytesIO(note.data).read()
    # write_bytesio_to_file('notetemp.md', content)
    # textfile = pypandoc.convert_file('notetemp.md', 'html', outputfile=f'noteviewtemp.html')
    return render_template('viewnote.html', title = 'Note', uid = uid, id = id, content = content)

@myapp_obj.route("/notetopdf/<int:id>", methods = ['GET', 'POST'])
def notetopdf(id):
    '''
    (not workring)
    Get a pdf of the current note

    This function will give the user a pdf copy of the current note they are viewing

    Parameter
    -------
    id : int
        The id of the currrent note
    '''
    note = Note.query.filter_by(id = id).first()
    content = BytesIO(note.data)
    write_bytesio_to_file('notetemp.md', content)
    filepdf = pypandoc.convert_file('notetemp.md', 'html', outputfile=f'{note.name}.pdf')
    return send_file(filepdf, attachment_filename=f'{note.name}.pdf', as_attachment=True)

@myapp_obj.route("/sharenote/<int:uid>/<int:id>", methods = ['GET', 'POST'])
def sharenote(uid, id):
    '''
    Share current note to another user

    This function will add a copy of the current note to the user whos name was inputed. It redirect the user to the note page afterwards

    Parameter
    -------
    uid : int
        The id of the user that is logged in
    id : int
        The id of the currrent note
    '''
    form = NoteShareForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.name.data).first()
        if user is None:
            flash('User does not exist')
        elif user.id is uid:
            flash('Cannot share with yourself')
        else:
            note = Note.query.filter_by(id = id).first()
            newnote = Note(name = note.name, data = note.data)
            newnote.set_user(user.id)
            db.session.add(newnote)
            db.session.commit()
            return redirect(f'/note/{uid}')
    return render_template('sharenote.html', title = 'Share note', form = form, uid = uid)

def write_bytesio_to_file(filename, bytesio): #code from TechOverflow
    '''
    Write to a file using a byteio object

    This function will write the contents of a byteio object into a file

    Parameter
    -------
    filename : String
        The name of the file that the be written onto
    bytesio : bytesio
        The object that contain the contents of a note file
    '''
    with open(filename, "wb") as outfile:
        outfile.write(bytesio.getbuffer())

@myapp_obj.route("/flashcardtopdf/<int:uid>")
def flashcardpdf(uid):
    '''
    (not working)
    Get a pdf of all of the user's flashcard

    This function will load a html page containing the all of the user's flashcard and provide them with a pdf of the page

    Parameter
    -------
    uid : int
        The id of the user that is logged in
    '''
    posts = []
    allCards = FlashCard.query.filter_by(User = uid).all()

    for x in range(len(allCards)): #sorting algorithm from GeeksforGeeks
        minRank = x
        for y in range(x+1, len(allCards)):
            if allCards[minRank].wrongguesscount < allCards[y].wrongguesscount:
                minRank = y     
        allCards[x], allCards[minRank] = allCards[minRank], allCards[x]

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
    rendered = render_template('flashcardtopdf.html', title = 'Flashcards', cardlist = posts, uid = uid)
    pdf = pdfkit.from_string(rendered, False)
    response = make_response(pdf)
    response.headers['content-type'] = 'application/pdf'
    response.headers['content-dispsition'] = 'inline; filename=output.pdf'
    return response