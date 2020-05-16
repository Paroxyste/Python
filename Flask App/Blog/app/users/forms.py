from app.models     import User
from flask_login    import current_user
from flask_wtf      import FlaskForm
from flask_wtf.file import FileAllowed, FileField

from wtforms import (BooleanField, PasswordField, StringField, 
                     SubmitField)

from wtforms.validators import (DataRequired, Email, EqualTo, Length, 
                               ValidationError)

# -----------------------------------------------------------------------------
# Login

class LoginForm(FlaskForm):

    email = StringField('Email',
                        validators = [DataRequired(), 
                                      Email()])

    password = PasswordField('Password', 
                             validators = [DataRequired()])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')

# -----------------------------------------------------------------------------
# Registration

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators = [DataRequired(), 
                                         Length(min = 2, max = 20)])

    email = StringField('Email',
                        validators = [DataRequired(), 
                                      Email()])

    password = PasswordField('Password', 
                             validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password',
                                     validators = [DataRequired(), 
                                                   EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()

        if user:
            raise ValidationError('''
                That username is taken. Please choose a
                different one.
            ''')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()

        if user:
            raise ValidationError('''
                That email is taken. Please choose a 
                different one.
            ''')

# -----------------------------------------------------------------------------
# Request Reset

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators = [DataRequired(), Email()])

    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()

        if user is None:
            raise ValidationError('''
                There is no account with that email. You must 
                register first.
            ''')

# -----------------------------------------------------------------------------
# Reset Password

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',
                             validators = [DataRequired()])

    conf_password = PasswordField('Confirm Password',
                                  validators = [DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Reset Password')

# -----------------------------------------------------------------------------
# Update Account

class UpdAccountForm(FlaskForm):
    username = StringField('Username',
                           validators = [DataRequired(), 
                                         Length(min = 2, max = 20)])

    email = StringField('Email',
                        validators = [DataRequired(), 
                                      Email()])

    picture = FileField('Update Profile Picture',
                        validators = [FileAllowed(['jpg', 'png', 'gif'])])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()

            if user:
                raise ValidationError('''
                    That username is taken. Please choose a 
                    different one.
                ''')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()

            if user:
                raise ValidationError('''
                    That email is taken. Please choose a 
                    different one.
                ''')