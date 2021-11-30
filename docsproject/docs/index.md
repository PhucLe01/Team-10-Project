# Welcome

Simply Study is a software that allow users to save notes, create flashcards, and keep track of task that they need to complete. 

# Information

Author: Phuc Le  
Github: [https://github.com/PhucLe01/Team-10-Project](https://github.com/PhucLe01/Team-10-Project)

# Installation

Users would need to go to the [Github repository](#information) and download all the files containing the code. User would also have to run the code through a Linux operating system with Python, Flask, and Sqlalchemy already installed.  

### Before running, install the following:  
* pip3 install pdfkit  
* sudo apt install wkhtmltopdf  
* pip3 install pypandoc  
* sudo apt-get install pandoc  

After installing everything, users can run the website by inputting "python3 run.py" into the command line.

# Features  
* Sign up/login of account  
    - Users can log into their account or sign up for an account.
* Delete account  
    - Users can delete their account while in the home page.
* Make a flashcard 
    - In the home page, users can click the createflash card button, fill in the nesscarity information and hit submit to create a flashcard.
* Order of flashcard will change depending on how many times user guess the flashcard right  
    - After viewing the description of a flashcard, users can click the right or wrong button depending on if they guess the description riht or not. This will re-order the flashcard on the home page where the card with the most wrong on top.
* Share flashcard with other users  
    - When viewing the description of a flashcard, users can click the share button and type in the name of another user to add the flashcard to their account.
* Get a pdf of all flashcard (incomplete)
    - When oon the homepage, users can click the get pdf of flashcard button to get a pdf of all of their flashcards.
* Upload and save markdown notes  
    - When on the home page, users can click the notes button to go to the notes menu where all of their notes are listed. In this page, users can click the upload notes button to have the option to upload a markdown file of their notes.
* Render saved markdown notes (incomplete)
    - When in the notes page, users can click on one of their notes to view the contents of that note.
* Share note with other users
    - When viewing the contents of a note, users can click the share button and type in the name of another user to add the note to their account.
* Get a pdf of note (incomplete)  
    - When viewing the contents of a note, users can click get pdf button to get a pdf of the note they are viewing.
* Set up task
    - When in the home page, User can click the task button to go to the task viewer. Users can click create task and fill in the information to create a task. After finishing a task, users can click mark as complete on the task to mark the task as complete.
* Pomodoro timer
    - When in the home page, users can click the 25 minute timer to begin a 25 minute countdown for studying. After the timer finishes, users can click on the 5 minute timer to start a 5 minute break timer. Users can repeat this if they choose to study more.

# Project layout  

    Team-10-Project                     # Folder containing all the files
        app/
            templates/                  # Templates for every pages in the website
                base.html
                createflashcard.html
                createtask.html
                description.html
                flashcardtopdf.html
                home.html
                login.html
                note.html
                pomodorostudy.html
                pomodorobreak.html
                shareflashcard.html
                sharenote.html
                signup.html
                taskview.html
                uploadnote.html
                viewnote.html
            __innit.py                  # Initialize website file
            forms.py                    # Form for all the website pages have need information input
            models.py                   # Database 
            routes.py                   # Routes for all the buttons and logic
        docsproject/
            docs/
                index.md                # The documentation homepage
            mkdocs.yml                  # The configuration file
        gantt.xlsx                      # Gantt chart
        run.py                          # File to start the website

# Code summary  
| forms.py file | Type | description |
|     ----      | ---- |    ----     |
| [LoginForm(FlaskForm)](#loginformflaskform) | class | The form for logging in |
| [SignUpForm(FlaskForm)](#signupformflaskform) | class | The form for signing up |
| [flashCardForm(FlaskForm)](#flashcardformflaskform) | class | The form for creating a flashcard |
| [FlashShareForm(FlaskForm)](#flashshareformflaskform) | class | The form for sharing a flashcard |
| [TaskForm(FlaskForm)](#taskformflaskform) | class | The form for creating a task |
| [NoteForm(FlaskForm)](#noteformflaskform) | class | The form for creating a note |
| [NoteShareForm(FlaskForm)](#noteshareformflaskform) | class | The form for sharing a note |

| models.py file | Type | description |
|     ----       | ---- |    ----     |
| [User(UserMixin, db.Model)](#userusermixin-dbmodel) | class | User database |
| [set_password(password)](#set_passwordpassword) | function | Set the password for the user |
| [check_password(password)](#check_passwordpassword) | fucntion | Check if the password if correct |
| [FlashCard(db.Model)](#flashcarddbmodel) | class |  Flashcard database |
| [set_user(uid)](#set_useruid-1) | function | Set the user for the flashcard |
| [inc_wrong_count()](#inc_wrong_count) | function | Inccrease wrongguesscount counter by 1 |
| [dec_wrong_count()](#dec_wrong_count) | function | Decrease wrongguesscount counter by 1 |
| [Task(db.Model)](#taskdbmodel) | class | Task database |
| [set_user(uid)](#set_useruid-2) | function | Set te user for the task |
| [set_startdate(startdate)](#set_startdatestartdate) | function | Set the start daet for the task |
| [set_deadline(deadline)](#set_deadlinedeadline) | function | Set the deadline for the task |
| [set_status()](#set_status) | function | Set the complete status of the task to true |
| [Note(db.Model)](#notedbmodel) | class | Note database |
| [set_user(uid)](#set_useruid-3) | function | Set the user for the note |

| routes.py file | Type | description |
|     ----       | ---- |    ----     |
| [begin()](#begin) | function | Start the website |
| [logout()](#logout) | fucntion | Log out of account |
| [login()](#login) | function | Log into account |
| [Signup()](#signup) | fucntion | Sign up for an account |
| [home(uid)](#homeuid) | function | Go to homepage |
| [createcard(uid)](#createcarduid) | function | Create a flashcard |
| [description(uid, id)](#descriptionuid-id) | function | Go to the description of the flashcard |
| [deleteaccount(uid)](#deleteaccountuid) | function | Delete account |
| [incwrongcount(uid, id)](#incwrongcountuid-id) | function | Use inc_wrong_count() to increase wrong guess count by 1 |
| [decwrongcount(uid, id)](#decwrongcountuid-id) | function | Use dec_wrong_count() to decrease wrong guess count by 1 |
| [shareflashcard(uid, id)](#shareflashcarduid-id) | function | Share flashcard with anotehr user |
| [taskviewer(uid)](#taskvieweruid) | function | View all task of the user |
| [createtask(uid)](#createtaskuid) | function | Create a task for the user |
| [finishtask(uid, id)](#finishtaskuid-id) | function | Mark a task as complete |
| [study(uid, t)](#studyuid-t) | function | Start a 25 minute timer |
| [breaktime(uid, t)](#breaktimeuid-t) | function | Start a 5 minute timer |
| [note(uid)](#noteuid) | function | View all notes of the user |
| [noteuploadpage(uid)](#noteuploadpageuid) | function | Upload and save a note file to the user's account |
| [viewnote(uid, id)](#viewnoteuid-id) | function | View the contents of the note |
| [notetopdf(id)](#notetopdfid) | function | Get a pdf of the note |
| [sharenote(uid, id)](#sharenoteuid-id) | function | Share the note with another user |
| [write_bytesio_to_file(filename, bytesio)](#write_bytesio_to_filefilename-bytesio) | function | Write the bytesio object to a file |
| [flashcardpdf(uid)](#flashcardpdfuid) | fucntion | Get a pdf of all the user's flashcard |

# Code functions and classes

### LoginForm(FlaskForm)
    '''
    This class contain the form for the login page
    '''

### SignUpForm(FlaskForm)
    '''
    This class contain the form for the sign up page
    '''

### flashCardForm(FlaskForm)
    '''
    This class contain the form for the flashcard creation page
    '''

### FlashShareForm(FlaskForm)
    '''
    This class contain the form for the share flashcard with other users page
    '''
### TaskForm(FlaskForm)
    '''
    This class contain the form for the create task page
    '''

### NoteForm(FlaskForm)
    '''
    This class contain the form for the upload markdown notes page
    '''

### NoteShareForm(FlaskForm)
    '''
    This class contain the form for the share note with other users page
    '''

### User(UserMixin, db.Model)
    '''
    The user database

    This keep track of the user's id, username, password, their flashcards, tasks, and notes
    '''

### set_password(password)
    '''
    Set the password

    This fuction set the password of the user after hashing the given value

    Parameters
    -------
    password : String
        input to be use as the password
    '''

### check_password(password)
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

### FlashCard(db.Model)
    '''
    The flashcard database

    This keep track of the flashcard's id, label, description, wrong guess count, and the id of the user it belongs to
    '''

### set_user(uid) [1]
    '''
    set the user of this flashcard

    Parameter
    -------
    uid : int
        The id of the user
    '''

### inc_wrong_count()
    '''
    Increase wrongguesscount by 1

    This function will increment the wrongguesscount counter of the flashcard by 1
    '''

### dec_wrong_count()
    '''
    Decrease wrongguesscount by 1

    This function will decrement the wrongguesscount counter of the flashcard by 1
    '''

### Task(db.Model)
    '''
    The task database

    This keep track of the task's id, label, startdate, dealine, complete status, and the id of the user it belongs to
    '''

### set_user(uid) [2]
    '''
    set the user of this task

    Parameter
    -------
    uid : int
        The id of the user
    '''

### set_startdate(startdate)
    '''
    set the startdate of this task

    Parameter
    -------
    startdate : date and time
        The start date for this task
    '''

### set_deadline(deadline)
    '''
    set the dealine of this task

    Parameter
    -------
    deadline : date and time
        The end date for this task
    '''

### set_status()
    '''
    Set status of the task to true
    '''

### Note(db.Model)
    '''
    The note database

    This keep track of the note's id, name, file data, and the user id it belongs to
    '''

### set_user(uid) [3]
    '''
    set the user of this note

    Parameter
    -------
    uid : int
        The id of the user
    '''

### begin()
    '''
    This start off the website

    This function will bring the user to the login page

    return
    -------
    redirect to /login
    '''

### logout()
    '''
    Log the user out

    This fucntion will log the user out of their account and redirect them to the login page

    return
    -------
    redirect /login
    '''

### login()
    '''
    Log the user in

    This fucntion will log the user into their account and bring them to the home page if the credentials are correct

    return
    -------
    Render template login.html and redirect to /home if successful
    Or
    redirect to itself if unsuccessful
    '''

### SignUp()
    '''
    Create an ccount

    This fuction will create an account if the input username and password are valid

    return
    -------
    Render template signup.html and redirect to /login if an account if created
    '''

### home(uid)
    '''
    The home page

    This function will bring the user to the home page where all their flashcard are listed in the order of their wrongguesscount

    Parameter
    -------
    uid : int
        The id of the user that is logged in

    return
    -------
    Redner template home.html
    '''

### createcard(uid)
    '''
    flashcard creation page

    This function bring the user to the flashcard creation page. A new flashcard will be created if the inputs are correct and  teh user is redirected to the homepage when done

    Parameter
    -------
    uid : int
        The id of the user that is logged in

    return
    -------
    Render template createflashcard.html and redirect to /home if a flashcard is created
    '''

### description(uid, id)
    '''
    The description of the flashcard

    This fucntion bring the user to a page that contain the description of the selected flashcard

    Parameter
    -------
    uid : int
        The id of the user that is logged in
    id : int
        The id of the flashcard that the user is seeing the description of

    return
    -------
    Render template description.html
    '''

### deleteAccount(uid)
    '''
    Delete the current account

    This function will delete the current account. It will redirect the user to the login page afterwards

    Parameter
    -------
    uid : int
        The id of the user that is logged in

    return
    -------
    Redirect to /login
    '''

### incwrongcount(uid, id)
    '''
    Increase the wrongguesscount 
    
    This function will increment the wrong guess count of the current flashcard by 1. It redirects the user to the homepage afterwards
    
    Parameter
    -------
    uid : int
        The id of the user that is logged in
    id : int
        The id of the currrent flashcard

    return
    -------
    Redirect to /home
    '''

### decwrongcount(uid, id)
    '''
    Decrease the wrongguesscount 
    
    This function will decrement the wrong guess count of the current flashcard by 1. It redirects the user to the homepage afterwards
    
    Parameter
    -------
    uid : int
        The id of the user that is logged in
    id : int
        The id of the currrent flashcard

    return
    -------
    Redirect to /home
    '''

### shareflashcard(uid, id)
    '''
    Share current flashcard to another user

    This function will add a copy of the current flashcard to the user whos name was inputed. It redirect the user to the homepage afterwards

    Parameter
    -------
    uid : int
        The id of the user that is logged in
    id : int
        The id of the currrent flashcard

    return
    -------
    Render template shareflashcard.html and redirect to /home if the flashcard was shared with another user
    '''

### taskviewer(uid)
    '''
    View all of the user's task

    This fucntion bring the user to the task page where all of their task are listed

    Parameter
    -------
    uid : int
        The id of the user that is logged in

    return
    -------
    Render template taskview.html
    '''

### createtask(uid)
    '''
    Create a task for the current user

    This function will create a task for the current user if the inputed name and dates are valid. It redirect teh user to the task page when done

    Parameter
    -------
    uid : int
        The id of the user that is logged in

    return
    -------
    Render template createtask.html and redirect to /taskviewer if a task was created
    '''

### finishtask(uid, id)
    '''
    Mark the task as complete

    This function will set the status of the selected task to complete

    Parameter
    -------
    uid : int
        The id of the user that is logged in
    id : int
        The id of the selected task

    return
    -------
    Redirect to /taskviewer
    '''

### study(uid, t)
    '''
    25 minute timer

    This function will bring the user to the 25 minute timer page and start the countdown

    Parameter
    -------
    uid : int
        The id of the user that is logged in
    t : int
        The time left on the timer in seconds

    return
    -------
    Render template pomodorostudy.html
    '''

### breaktime(uid, t)
    '''
    5 minute timer

    This function will bring the user to the 5 minute timer page and start the countdown

    Parameter
    -------
    uid : int
        The id of the user that is logged in
    t : int
        The time left on the timer in seconds

    return
    -------
    Render template pomodorobreak.html
    '''

### note(uid)
    '''
    View all fo the user's note files

    This fucntion bring the user to the note page where all of their notes are listed

    Parameter
    -------
    uid : int
        The id of the user that is logged in

    return
    -------
    Render template note.html
    '''

### noteuploadpage(uid)
    '''
    Upload file

    This fucntion bring the user to the upload file page and will save the uploaded note file to the current user's account

    Parameter
    -------
    uid : int
        The id of the user that is logged in

    return
    -------
    Render template uploadnote.html
    '''

### viewnote(uid, id)
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

    return
    -------
    Render template viewnote.html
    '''

### notetopdf(id)
    '''
    (not workring)
    Get a pdf of the current note

    This function will give the user a pdf copy of the current note they are viewing

    Parameter
    -------
    id : int
        The id of the currrent note

    return
    -------
    PDF file 
    '''

### sharenote(uid, id)
    '''
    Share current note to another user

    This function will add a copy of the current note to the user whos name was inputed. It redirect the user to the note page afterwards

    Parameter
    -------
    uid : int
        The id of the user that is logged in
    id : int
        The id of the currrent note

    return
    -------
    Render template sharenote.html
    '''

### write_bytesio_to_file(filename, bytesio)
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

### flashcardpdf(uid)
    '''
    (not working)
    Get a pdf of all of the user's flashcard

    This function will load a html page containing the all of the user's flashcard and provide them with a pdf of the page

    Parameter
    -------
    uid : int
        The id of the user that is logged in

    return
    -------
    PDF file
    '''