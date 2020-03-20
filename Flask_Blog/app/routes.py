from flask import render_template, url_for, flash, redirect
from app import app
from app.forms import RegistrationForm, LoginForm
from app.models import User, Post

posts = [
    {
        'author': 'Laurent Echeverria',
        'title': 'Hello There !',
        'content': 'This is my first post content',
        'date_posted': '20 Mars 2020'
    },
    {
        'author': 'John Doe',
        'title': 'Hello World',
        'content': 'This is the second post content',
        'date_posted': 'April 21, 2018'
    }
]

# Root ------------------------------------------------------------------------

@app.route("/")
@app.route("/home")

def home():
    return render_template('home.html', 
                            posts = posts)

# About -----------------------------------------------------------------------

@app.route("/about")

def about():
    return render_template('about.html', 
                            title = 'About')

# Register --------------------------------------------------------------------

@app.route("/register", methods = ['GET', 'POST'])

def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', 
                            title = 'Register', 
                            form = form)

# Login -----------------------------------------------------------------------

@app.route("/login", methods=['GET', 'POST'])

def login():
    form = LoginForm()

    if form.validate_on_submit():
        if form.email.data == 'contact@mail.fr' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', 
                            title = 'Login', 
                            form = form)