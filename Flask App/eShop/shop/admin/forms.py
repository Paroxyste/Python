from .models   import User
from flask_wtf import FlaskForm, Form
from wtforms   import BooleanField, PasswordField, StringField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError

# -----------------------------------------------------------------------------
# Login

def login_form(FlaskForm):
    email = StringField('Email Adress', 
                        validators=[DataRequired(),
                                    Length(min=6, max=35)])

    password = PasswordField('Password',
                             validators=[DataRequired()])

# -----------------------------------------------------------------------------
# Registration

def register_form(FlaskForm):
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

    def validate_username(self, field):
        if (User.query.filter_by(username=field.data).first()):
            raise ValidationError('Username already in use.')

    def validate_email(self, field):
        if (User.query.filter_by(email=field.data).first()):
            raise ValidationError('Email already registred.')