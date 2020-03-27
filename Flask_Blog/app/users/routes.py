from app             import bcrypt, db
from app.models      import Post, User
from app.users.forms import (LoginForm, RegistrationForm, RequestResetForm,
                             ResetPasswordForm, UpdAccountForm)
from app.users.utils import save_picture, send_reset_email

from flask import (Blueprint, flash, redirect, render_template,
                  request, url_for)

from flask_login import (current_user, login_user, login_required,
                         logout_user)

# -----------------------------------------------------------------------------
# About

@users.route("/about")

def about():
    return render_template('about.html', 
                           title = 'About')

# -----------------------------------------------------------------------------
# Account

@users.route("/account",
           methods = ['GET', 'POST'])

@login_required

def account():
    form = UpdAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()
        flash('Your account has been updated !',
              'success')

        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', 
                         filename = 'profile_pics/' + current_user.image_file)

    return render_template('account.html', 
                           title = 'Account',
                           form  = form,
                           image_file = image_file)

# -----------------------------------------------------------------------------
# Login

@users.route("/login", 
           methods = ['GET', 'POST'])

def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, 
                                               form.password.data):
            login_user(user, remember = form.remember.data)

            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Failed ! Please check email and password.', 
                  'danger')

    return render_template('login.html', 
                           title = 'Login',
                           form  = form)

# -----------------------------------------------------------------------------
# Logout

@users.route("/logout")

def logout():
    logout_user()

    return redirect(url_for('main.home'))


# -----------------------------------------------------------------------------
# Post : Post by Username

@users.route("/user/<string:username>")

def user_posts(username):
    page = request.args.get('page', 1, type = int)

    user = User.query.filter_by(username = username).first_or_404()

    posts = Post.query.filter_by(author = user)\
                      .order_by(Post.date_posted.desc())\
                      .paginate(page = page, per_page = 5)

    return render_template('user_post.html', 
                           posts = posts,
                           user  = user)