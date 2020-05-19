from .models        import Register
from flask_wtf      import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms        import (Form, PasswordField, StringField, SubmitField,
                            TextAreaField)

from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)

# -----------------------------------------------------------------------------
# Customer Login

class CustomerLoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), 
                                    Email(),
                                    Length(min=6, max=50)])

    password = PasswordField('Password',
                             validators=[DataRequired()])

# -----------------------------------------------------------------------------
# Customer Register

class CustomerRegisterForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(),
                                   Length(min=3, max=50)])

    username = StringField('Username',
                           validators=['Username',
                                       DataRequired(),
                                       Length(min=3, max=50)])

    email = StringField('Email',
                         validators=[DataRequired(),
                                     Length(min=3, max=50),
                                     Email()])

    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         EqualTo('confirm',
                                                 message='Both password must \
                                                          match !')])

    country = StringField('Country',
                          validators=[DataRequired(),
                                      Length(min=3, max=50)])

    city = StringField('City',
                       validators=[DataRequired(),
                                   Length(min=3, max=50)])

    contact = StringField('Contact',
                          validators=[DataRequired(),
                                      Length(min=3, max=50)])

    address = StringField('Address',
                          validators=[DataRequired(),
                                      Length(min=3, max=50)])

    zipode = StringField('Zip Code',
                        validators=[DataRequired(),
                                    Length(min=3, max=10)])

    profile = FileField('Profile',
                        validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'],
                                                'Image only please !')])

    submit = SubmitField('Register')

    # Check username to database
    def validate_username(self, username):
        if (Register.query.filter_by(username=username.data).first()):
            raise ValidationError('This username is already in use !')

    # Check email to database
    def validate_email(self, email):
        if (Register.query.filter_by(email=email.data).first()):
            raise ValidationError('This email address is already in use !')
