# -----------------------------------------------------------------------------

import re

# -----------------------------------------------------------------------------

def form_email_check(email):
    msg_err = None

    if (len(email) < 10 or len(email) > 50):
        msg_err = (
            'Email address must contain between 10 '
            'and 50 characters !'
        )

    elif not re.fullmatch(r'[^@]+@[^@]+\.[^@]+', email):
        msg_err = 'Invalid email address !'

    return msg_err

# -----------------------------------------------------------------------------

def form_email_cleaner(my_str):
    my_str = re.sub('[!#$%^&*()[]{};:,/<>?\|`~=+ \n\.]', '', my_str)

    return my_str

# -----------------------------------------------------------------------------

def form_password_check(password):
    msg_err = None

    if (len(password) < 10 or len(password) > 60):
        msg_err = (
            'Length of the password must be between 10 '
            'and 60 characters !'
        )

    return msg_err

# -----------------------------------------------------------------------------

def form_str_cleaner(my_str):
    my_str = re.sub('[^a-zA-Z0-9 \n\.]', '', my_str)

    return my_str

# -----------------------------------------------------------------------------

def form_username_check(username):
    msg_err = None

    if (len(username) < 3 or len(username) > 25):
        msg_err = (
            'Username must contain between 3 '
            'and 25 characters !'
        )

    elif not re.fullmatch(r'[A-Za-z0-9]+', username):
        msg_err = 'Username must contain only characters and numbers !'

    return msg_err