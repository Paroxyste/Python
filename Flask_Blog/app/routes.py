from flask import render_template, url_for, flash, redirect
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User, Post
from flask_login import login_user, current_user

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

@app.route("/register", 
           methods = ['GET', 'POST'])

def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hash_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(username = form.username.data, 
                    email = form.email.data,
                    password = hash_pass)

        db.session.add(user)
        db.session.commit()

        flash(f'Your account has been created ! Your are now able to login', 
                'success')

        return redirect(url_for('login'))

    return render_template('register.html', 
                           title = 'Register', 
                           form = form)

# Login -----------------------------------------------------------------------

@app.route("/login", 
           methods = ['GET', 'POST'])

def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)

            return redirect(url_for('home'))
        else:
            flash('Login Failed ! Please check email and password.', 
                  'danger')

    return render_template('login.html', 
                           title = 'Login', 
                           form = form)