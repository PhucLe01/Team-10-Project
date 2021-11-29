# Welcome

Simply Study is a software that allow users to save notes, create flashcards, and keep track of task that they need to complete. 

# Information

Author: Phuc Le  
Github: [https://github.com/PhucLe01/Team-10-Project](https://github.com/PhucLe01/Team-10-Project)

# Installation

Users would need to go to the [Github repository](#information) and download all the files containing the code. User would also have to run the code through a Linux operating system with Python, Flask, and Sqlalchemy already installed.  

##### Before running, install the following:  
* pip3 install pdfkit  
* sudo apt install wkhtmltopdf  
* pip3 install pypandoc  
* sudo apt-get install pandoc  

# Features

# Code summary  
| forms.py file | Type | description |
|     ---       | ---- |    ----     |
| [LoginForm(FlaskForm)](###LoginForm(FlaskForm)) | class | The form for logging in |
| [SignUpForm(FlaskForm)] | class | The form for signing up |
| [flashCardForm(FlaskForm)] | class | The form for creating a flashcard |
| [FlashShareForm(FlaskForm)] | class | The form for sharing a flashcard |
| [TaskForm(FlaskForm)] | class | The form for creating a task |
| [NoteForm(FlaskForm)] | class | The form for creating a note |
| [NoteShareForm(FlaskForm)] | class | The form for sharing a note |

| models.py file | Type | description |
|     ----       | ---- |    ----     |
| [User(UserMixin, db.Model)] | class | User database |
| [set_password(password)] | function | Set the password for the user |
| [check_password(password)] | fucntion | Check if the password if correct |
| [FlashCard(db.Model)] | class |  Flashcard database |
| [set_user(uid)] | function | Set the user for the flashcard |
| [inc_wrong_count()] | function | Inccrease wrongguesscount counter by 1 |
| [dec_wrong_count()] | function | Decrease wrongguesscount counter by 1 |
| [Task(db.Model)] | class | Task database |
| [set_user(uid)] | function | Set te user for the task |
| [set_startdate(startdate)] | function | Set the start daet for the task |
| [set_deadline(deadline)] | function | Set the deadline for the task |
| [set_status(self)] | function | Set the complete status of the task to true |
| [Note(db.Model)] | class | Note database |
| [set_user(uid)] | function | Set the user for the note |

| routes.py file | Type | description |
|     ----       | ---- |    ----     |
| [begin()] | function | Start the website |
| [logout()] | fucntion | Log out of account |
| [login()] | function | Log into account |
| [Signup()] | fucntion | Sign up for an account |
| [home(uid)] | function | Go to homepage |
| [createcard(uid)] | function | Create a flashcard |
| [description(uid, id)] | function | Go to the description of the flashcard |
| [deleteaccount(uid)] | function | Delete account |
| [incwrongcount(uid, id)] | function | Use inc_wrong_count() to increase wrong guess count by 1 |
| [decwrongcount(uid, id)] | function | Use dec_wrong_count() to decrease wrong guess count by 1 |
| [shareflashcard(uid, id)] | function | Share flashcard with anotehr user |
| [taskviewer(uid)] | function | View all task of the user |
| [createtask(uid)] | function | Create a task for the user |
| [finishtask(uid, id)] | function | Mark a task as complete |
| [study(uid, t)] | function | Start a 25 minute timer |
| [breaktime(uid, t)] | function | Start a 5 minute timer |
| [note(uid)] | function | View all notes of the user |
| [noteuploadpage(uid)] | function | Upload and save a note file to the user's account |
| [viewnote(uid, id)] | function | View the contents of the note |
| [notetopdf(id)] | function | Get a pdf of the note |
| [sharenote(uid, id)] | function | Share the note with another user |
| [write_bytesio_to_file(filename, bytesio)] | function | Write the bytesio object to a file |
| [flashcardpdf(uid)] | fucntion | Get a pdf of all the user's flashcard |

# Code functions and classes

### LoginForm(FlaskForm)
    '''
    This class contain the form for the login page
    '''