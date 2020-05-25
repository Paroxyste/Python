from .models   import Admin
from flask_wtf import FlaskForm, Form
from wtforms   import BooleanField, PasswordField, StringField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError

# -----------------------------------------------------------------------------
# Admin Login

class LoginForm(FlaskForm):
    email = StringField('Email Adress', 
                        validators=[DataRequired(),
                                    Length(min=6, max=35)])

    password = PasswordField('Password',
                             validators=[DataRequired()])

# -----------------------------------------------------------------------------
# Admin Register

class RegisterForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(),
                                   Length(min=4, max=25)])

    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=4, max=25)])

    email = StringField('Email Adress',
                        validators=[DataRequired(),
                                    Length(min=6, max=35)])

    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         EqualTo('confirm', 
                                                 message='Passwords must \
                                                          match')])

    confirm = PasswordField('Repeat Password',
                            validators=[DataRequired()])

    # Check username to database
    def validate_username(self, field):
        if (Admin.query.filter_by(username=field.data).first()):
            raise ValidationError('This username is already in use !')

    # Check email to database
    def validate_email(self, field):
        if (Admin.query.filter_by(email=field.data).first()):
            raise ValidationError('This email address is already in use !')