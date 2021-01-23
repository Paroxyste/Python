from .security             import pwd_context

from datetime              import date

from easyml._init_         import mysql

from easyml.utils.datas    import datas_cat_nav
from easyml.utils.datas    import datas_mod_nav
from easyml.utils.datas    import datas_set_nav

from easyml.utils.form     import form_email_check
from easyml.utils.form     import form_email_cleaner
from easyml.utils.form     import form_password_check
from easyml.utils.form     import form_str_cleaner
from easyml.utils.form     import form_username_check

from easyml.utils.users    import user_add
from easyml.utils.users    import user_del_account
from easyml.utils.users    import user_del_session
from easyml.utils.users    import user_details
from easyml.utils.users    import user_register_date
from easyml.utils.users    import user_upd_email
from easyml.utils.users    import user_upd_last_connection
from easyml.utils.users    import user_upd_lang
from easyml.utils.users    import user_upd_pass
from easyml.utils.users    import user_upd_username

from flask                 import Blueprint
from flask                 import redirect
from flask                 import render_template
from flask                 import request
from flask                 import session

import MySQLdb.cursors

# -----------------------------------------------------------------------------
# Init users

users = Blueprint('users', __name__)

# -----------------------------------------------------------------------------
# Delete Account

@users.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    msg_suc = None

    # Check if user is loggedin
    if ('loggedin' in session):

        # Get session details
        username = session['username']
        email    = session['email']
        lang     = session['lang']

        if (request.method == 'POST'):

            # Connect to database
            cursor = mysql.connection.cursor()

            msg_suc = user_del_account(cursor, username, email, lang)
            user_del_session()

            # Break connection
            cursor.close()

            return render_template(
                'users/logout.html',
                title='Account Deleted',
                lang=lang,
                msg_suc=msg_suc
            )

        return render_template(
            'users/delete_account.html',
            title='EasyML - Delete Account',
            lang=lang
        )

    else:
        return redirect('404')

# -----------------------------------------------------------------------------
# Login

@users.route('/login', methods=['GET', 'POST'])
def login():
    msg_err, msg_suc = (None,) * 2

    # Case 1 : Complete login form
    if (request.method == 'POST'
        and bool(request.form['email'])    == 1
        and bool(request.form['password']) == 1
    ):
        email    = request.form['email'].lower()
        password = request.form['password']

        # Email form verification
        msg_err = form_email_check(email)

        # Password form verification
        msg_err = form_password_check(password)

        if (msg_err is None):
            # Connect to database
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # Get user_details
            user_infos      = user_details(cursor, email, None)
            query_count_res = cursor.rowcount

            # Check if query contain result
            if (query_count_res > 0):

                # Get user details
                username    = user_infos[1]
                email       = user_infos[2]
                hashed_pass = user_infos[3]
                lang        = user_infos[4]

                # Verify password POST and hashed password
                pass_verify = pwd_context.verify(password, hashed_pass)

                if (bool(pass_verify == 1)):
                    # Update last connection date
                    date_now = date.today().strftime('%Y-%m-%d')
                    user_upd_last_connection(cursor, username, email, date_now)

                    # Break connection
                    cursor.close()

                    # Create session data
                    session['loggedin'] = True
                    session['username'] = username.capitalize()
                    session['email']    = email
                    session['lang']     = lang.lower()

                    # Success
                    msg_suc = 'Logged in successfully !'

                else:
                    msg_err = 'Incorrect email or password !'
                    cursor.close()

            else:
                msg_err = 'Incorrect email or password !'
                cursor.close()


    # Case 2 : One or more field missing
    elif (request.method == 'POST'
          and (bool(request.form['email'])    == 0
          or   bool(request.form['password']) == 0)
    ):
        msg_err = 'All fields are required !'

    return render_template(
        'users/login.html', 
        title='EasyML - Login',
        msg_err=msg_err,
        msg_suc=msg_suc
    )

# -----------------------------------------------------------------------------
# Logout

@users.route('/logout')
def logout():
    # Check if user is loggedin
    if ('loggedin' in session):

        # Remove session data, this will log the user out
        user_del_session()

        return render_template(
            'users/logout.html',
            title='EasyML - Logout',
            msg_suc=None
        )

    else:
        return redirect('404')

# -----------------------------------------------------------------------------
# Register

@users.route('/register',  methods=['GET', 'POST'])
def register():
    msg_err, msg_suc = (None,) * 2

    # Case 1 : All fields was complete
    if (request.method == 'POST'
        and bool(request.form['username']) == 1
        and bool(request.form['email'])    == 1
        and bool(request.form['password']) == 1
        and bool(request.form['lang_sel']) == 1
    ):
        username = form_str_cleaner(request.form['username'].lower())
        email    = form_email_cleaner(request.form['email'].lower())
        password = request.form['password']
        lang     = form_str_cleaner(request.form['lang_sel'].upper())

        # Username form verification
        msg_err = form_username_check(username)

        # Email form verification
        msg_err = form_email_check(email)

        # Password form verification
        msg_err = form_password_check(password)

        if (msg_err is None):
            # Connect to database
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            query = (
                'SELECT username '
                'FROM users '
                'WHERE (username = %s OR email = %s);'
            )

            cursor.execute(query, (username, email))

            # Fetch num of record
            query_count_res = cursor.rowcount

            # No account found
            if (query_count_res == 0):

                # Encrypt password
                password = pwd_context.encrypt(password)

                # Get datetime of registration
                register_date = user_register_date()

                msg_suc = user_add(cursor, username, email, password, register_date, lang)

                # Break connection
                cursor.close()

            else:
                msg_err = 'Username or email already exists !'
                cursor.close()

    # Case 2 : One field or more fields was missing
    elif (request.method == 'POST'
        and (bool(request.form['username']) == 0
        or   bool(request.form['email'])    == 0
        or   bool(request.form['password']) == 0
        or   bool(request.form['lang_sel']) == 0)
    ):
        msg_err = 'All fields are required !'

    return render_template(
        'users/register.html',
        title='EasyML - Register',
        msg_err=msg_err,
        msg_suc=msg_suc
    )

# -----------------------------------------------------------------------------
# Settings

@users.route('/settings', methods = ['GET', 'POST'])
def settings():
    msg_err, msg_suc = (None,) * 2

    # Check if user is loggedin
    if ('loggedin' in session):

        # Get session details
        username = session['username']
        email    = session['email']
        lang     = session['lang']

        # Connect to database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Get categories of navbar
        navbar_cat      = datas_cat_nav(cursor, lang)
        navbar_cat_name = navbar_cat[0]
        navbar_cat_tag  = navbar_cat[1]
        navbar_cat_icon = navbar_cat[2]
        navbar_cat_link = navbar_cat[3]

        # Get models of navbar
        navbar_models = datas_mod_nav(cursor, lang, navbar_cat_tag)

        # Get settings of navbar
        navbar_settings = datas_set_nav(cursor, lang)
        navbar_set_name = navbar_settings[0]
        navbar_set_icon = navbar_settings[1]
        navbar_set_link = navbar_settings[2]

        # Case 1 : Update all fields
        if (request.method == 'POST'
            and bool(request.form['username'])     == 1
            and bool(request.form['email'])        == 1
            and bool(request.form['password'])     == 1
            and bool(request.form['new_password']) == 1
        ):
            new_username = form_str_cleaner(request.form['username'].lower())
            new_email    = form_email_cleaner(request.form['email'].lower())
            password     = request.form['password']
            new_password = request.form['new_password']
            new_lang     = request.form['lang_sel'].upper()

            # Username form verification
            msg_err = form_username_check(username)

            # Email form verification
            msg_err = form_email_check(email)

            # Password form verification
            msg_err = form_password_check(password)
            msg_err = form_password_check(new_password)

            if (msg_err is None):
                # Connect to database
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

                # Get user_details
                user_infos      = user_details(cursor, new_email, new_username)
                query_count_res = cursor.rowcount

                # No account found
                if (query_count_res == 0):

                    # Get user_details
                    user_infos      = user_details(cursor, email, username)
                    query_count_res = cursor.rowcount

                    if (query_count_res > 0):

                        # Verify old password
                        hashed_pass = user_infos[4]
                        pass_verify = pwd_context.verify(password, hashed_pass)

                        if (bool(pass_verify == 1)):
                            # Encrypt new_password
                            new_password = pwd_context.encrypt(new_password)

                            query = (
                                'UPDATE users '
                                'SET username = %s, email = %s, password = %s '
                                'WHERE (username = %s AND email = %s);'
                            )

                            cursor.execute(query, (new_username, new_email, new_password, username, email))

                            # Commit to DB
                            mysql.connection.commit()

                            if (new_lang != lang.upper()):
                                user_upd_lang(cursor, new_lang, username, email)

                            if (lang == 'en'):
                                # Success
                                msg_suc = 'All fields was successfully updated !'

                            else:
                                msg_suc = (
                                    'Tous les champs ont été mis à jour '
                                    ' avec succès !'
                                )

                            # Break connection
                            cursor.close()

                        else:
                            if (lang == 'en'):
                                msg_err = 'Old password is invalid !'
                            else:
                                msg_err = (
                                    'L\'ancien mot de passe n\'est '
                                    'pas valide !'
                                )
                            cursor.close()

                    else:
                        if (lang == 'en'):
                            msg_err = 'An error was occurred !'
                        else:
                            msg_err = 'Une erreur s\'est produite !'
                        cursor.close()

                else:
                    if (lang == 'en'):
                        msg_err = 'Username or email already exists !'
                    else:
                        msg_err = (
                            'Le nom d\'utilisateur ou l\'adresse '
                            'mail existe déjà !'
                        )
                    cursor.close()

        # Case 2 : Update username + email + lang
        elif (request.method == 'POST'
              and bool(request.form['username'])     == 1
              and bool(request.form['email'])        == 1
              and bool(request.form['password'])     == 0
              and bool(request.form['new_password']) == 0
        ):
            new_username = form_str_cleaner(request.form['username'].lower())
            new_email    = form_email_cleaner(request.form['email'].lower())
            new_lang     = request.form['lang_sel'].upper()

            # Username form verification
            msg_err = form_username_check(username)

            # Email form verification
            msg_err = form_email_check(email)

            if (msg_err is None):
                # Connect to database
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

                # Get user_details
                user_infos      = user_details(cursor, new_email, new_username)
                query_count_res = cursor.rowcount

                # No account found
                if (query_count_res == 0):
                    query = (
                        'UPDATE users '
                        'SET username = %s, email = %s '
                        'WHERE (username = %s AND email = %s);'
                    )

                    cursor.execute(query, (new_username, new_email, username, email))

                    # Commit to DB
                    mysql.connection.commit()

                    if (new_lang != lang.upper()):
                        user_upd_lang(cursor, new_lang, username, email)

                        if (lang == 'en'):
                            # Success
                            msg_suc = (
                                'Username, email and language was '
                                'successfully updated !'
                            )

                        else:
                            msg_suc = (
                                'Le nom d\'utilisateur, l\'adresse '
                                'mail et la langue ont été mis à jour '
                                'avec succès !'
                            )

                        # Break connection
                        cursor.close()

                    else:
                        if (lang == 'en'):
                            # Success
                            msg_suc = (
                                'Username and email was successfully '
                                'updated !'
                            )
                        
                        else:
                            msg_suc = (
                                'Le nom d\'utilisateur et l\'adresse '
                                'mail ont été mis à jour avec succès !'
                            )

                        # Break connection
                        cursor.close()

                else :
                    if (lang == 'en'):
                        msg_err = 'Username or email already exists !'
                    else:
                        msg_err = (
                            'Le nom d\'utilisateur ou l\'adresse '
                            'mail existe déjà !'
                        )
                    cursor.close()

        # Case 3 : Update username + password + lang
        elif (request.method == 'POST'
              and bool(request.form['username'])     == 1
              and bool(request.form['email'])        == 0
              and bool(request.form['password'])     == 1
              and bool(request.form['new_password']) == 1
        ):
            new_username = form_str_cleaner(request.form['username'].lower())
            password     = request.form['password']
            new_password = request.form['new_password']
            new_lang     = request.form['lang_sel'].upper()

            # Username form verification
            msg_err = form_username_check(username)

            # Password form verification
            msg_err = form_password_check(password)

            if (msg_err is None):
                # Connect to database
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

                # Get user_details
                user_infos      = user_details(cursor, None, new_username)
                query_count_res = cursor.rowcount

                # No account found
                if (query_count_res == 0):

                    # Get user_details
                    user_infos      = user_details(cursor, email, username)
                    query_count_res = cursor.rowcount

                    if (query_count_res > 0):

                        # Verify old password
                        hashed_pass = user_infos[4]
                        pass_verify = pwd_context.verify(password, hashed_pass)

                        if (bool(pass_verify == 1)):

                            # Encrypt new_password
                            new_password = pwd_context.encrypt(new_password)

                            query = (
                                'UPDATE users '
                                'SET username = %s, password = %s '
                                'WHERE (username = %s AND email = %s);'
                            )

                            cursor.execute(query, (new_username, new_password, username, email))

                            # Commit to DB
                            mysql.connection.commit()

                            if (new_lang != lang.upper()):
                                user_upd_lang(cursor, new_lang, username, email)

                                if (lang == 'en'):
                                    # Success
                                    msg_suc = (
                                        'Username, password and language was '
                                        'successfully updated !'
                                    )
                                else:
                                    msg_suc = (
                                        'Le nom d\'utilisateur, le mot de '
                                        'passe et la langue ont été mis à jour '
                                        'avec succès !'
                                    )

                                # Break connection
                                cursor.close()

                            else:
                                if (lang == 'en'):
                                    # Success
                                    msg_suc = (
                                        'Username and password was successfully '
                                        'updated !'
                                    )
                                
                                else:
                                    msg_suc = (
                                        'Le nom d\'utilisateur et le mot de '
                                        'passe ont été mis à jour avec succès !'
                                    )

                            # Break connection
                            cursor.close()

                        else:
                            if (lang == 'en'):
                                msg_err = 'Old password is invalid !'
                            else:
                                msg_err = (
                                    'L\'ancien mot de passe n\'est '
                                    'pas valide !'
                                )
                            cursor.close()

                    else:
                        if (lang == 'en'):
                            msg_err = 'An error was occurred !'
                        else:
                            msg_err = 'Une erreur s\'est produite !'
                        cursor.close()

                else:
                    if (lang == 'en'):
                        msg_err = 'Username already exists !'
                    else:
                        msg_err = 'Le nom d\'utilisateur existe déjà !'

                    cursor.close()

        # Case 4 : Update email + password + lang
        elif (request.method == 'POST'
              and bool(request.form['username'])     == 0
              and bool(request.form['email'])        == 1
              and bool(request.form['password'])     == 1
              and bool(request.form['new_password']) == 1
        ):
            new_email    = form_email_cleaner(request.form['email'].lower())
            password     = request.form['password']
            new_password = request.form['new_password']
            new_lang     = request.form['lang_sel'].upper()

            # Email form verification
            msg_err = form_email_check(email)

            # Password form verification
            msg_err = form_password_check(password)

            if (msg_err is None):
                # Connect to database
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

                # Get user_details
                user_infos      = user_details(cursor, new_email, None)
                query_count_res = cursor.rowcount

                # No account found
                if (query_count_res == 0):

                    # Get user_details
                    user_infos      = user_details(cursor, email, username)
                    query_count_res = cursor.rowcount

                    if (query_count_res > 0):

                        # Verify old password
                        hashed_pass = user_infos[4]
                        pass_verify = pwd_context.verify(password, hashed_pass)

                        if (bool(pass_verify == 1)):

                            # Encrypt new_password
                            new_password = pwd_context.encrypt(new_password)

                            query = (
                                'UPDATE users '
                                'SET email = %s, password = %s '
                                'WHERE (username = %s AND email = %s);'
                            )

                            cursor.execute(query, (new_email, new_password, username, email))

                            # Commit to DB
                            mysql.connection.commit()

                            if (new_lang != lang.upper()):
                                user_upd_lang(cursor, new_lang, username, email)

                                if (lang == 'en'):
                                    # Success
                                    msg_suc = (
                                        'Email, password and language was '
                                        'successfully updated !'
                                    )

                                else:
                                    msg_suc = (
                                        'L\'adresse mail, le mot de passe et '
                                        'la langue ont été mis à jour avec '
                                        'succès !'
                                    )

                                # Break connection
                                cursor.close()

                            else:
                                if (lang == 'en'):
                                    # Success
                                    msg_suc = (
                                        'Email and password was successfully '
                                        'updated !'
                                    )

                                else:
                                    msg_suc = (
                                        'L\'adresse mail et le mot de passe '
                                        'ont été mis à jour avec succès !'
                                    )

                                # Break connection
                                cursor.close()

                        else:
                            if (lang == 'en'):
                                msg_err = 'Old password is invalid !'
                            else:
                                msg_err = (
                                    'L\'ancien mot de passe n\'est '
                                    'pas valide !'
                                )
                            cursor.close()

                    else:
                        if (lang == 'en'):
                            msg_err = 'An error was occurred !'
                        else:
                            msg_err = 'Une erreur s\'est produite !'
                        cursor.close()

                else:
                    if (lang == 'en'):
                        msg_err = 'Email already exists !'
                    else:
                        msg_err = 'L\'adresse mail existe déjà !'

                    cursor.close()

        # Case 5 : Update username + lang
        elif (request.method == 'POST'
              and bool(request.form['username'])     == 1
              and bool(request.form['email'])        == 0
              and bool(request.form['password'])     == 0
              and bool(request.form['new_password']) == 0
        ):
            new_username = form_str_cleaner(request.form['username'].lower())
            new_lang     = request.form['lang_sel'].upper()

            # Username form verification
            msg_err = form_username_check(username)

            if (msg_err is None):
                # Connect to database
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

                # Get user_details
                user_infos      = user_details(cursor, None, new_username)
                query_count_res = cursor.rowcount

                # No account found
                if (query_count_res == 0):
                    user_upd_username(cursor, new_username, username, email)

                    if (new_lang != lang.upper()):
                        user_upd_lang(cursor, new_lang, username, email)

                        if (lang == 'en'):
                            # Success
                            msg_suc = (
                                'Username and language was successfully updated !'
                            )

                        else:
                            msg_suc = (
                                'Le nom d\'utilisateur et la langue '
                                'ont été mis à jour avec succès !'
                            )

                        # Break connection
                        cursor.close()

                    else:
                        if (lang == 'en'):
                            # Success
                            msg_suc = 'Username was successfully updated !'

                        else:
                            msg_suc = (
                                'Le nom d\'utilisateur a été mis à jour avec succès !'
                            )

                        # Break connection
                        cursor.close()

                else:
                    if (lang == 'en'):
                        # Success
                        msg_err = 'Username already exists !'

                    else:
                        msg_err = (
                            'Le nom d\'utilisateur existe déjà !'
                        )

                    cursor.close()

        # Case 6 : Update email + lang
        elif (request.method == 'POST'
              and bool(request.form['username'])     == 0
              and bool(request.form['email'])        == 1
              and bool(request.form['password'])     == 0
              and bool(request.form['new_password']) == 0
        ):
            new_email = form_email_cleaner(request.form['email'].lower())
            new_lang  = request.form['lang_sel'].upper()

            # Email form verification
            msg_err = form_email_check(email)

            if (msg_err is None):
                # Connect to database
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

                # Get user_details
                user_infos      = user_details(cursor, new_email, None)
                query_count_res = cursor.rowcount

                # No account found
                if (query_count_res == 0):
                    user_upd_email(cursor, new_email, username, email)

                    if (new_lang != lang.upper()):
                        user_upd_lang(cursor, new_lang, username, email)

                        if (lang == 'en'):
                            # Success
                            msg_suc = (
                                'Email and language was successfully updated !'
                            )

                        else:
                            msg_suc = (
                                'L\' adresse mail et la langue ont été mis '
                                'à jour avec succès !'
                            )

                        # Break connection
                        cursor.close()

                    else:
                        if (lang == 'en'):
                            # Success
                            msg_suc = 'Email was successfully updated !'

                        else:
                            msg_suc = (
                                'L\' adresse mail a été mis à jour avec succès !'
                            )

                        # Break connection
                        cursor.close()

                else:
                    if (lang == 'en'):
                        # Success
                        msg_err = 'Email already exists !'

                    else:
                        msg_err = (
                            'L\' adresse mail existe déjà !'
                        )

                    cursor.close()

        # Case 7 : Update password + lang
        elif (request.method == 'POST'
              and bool(request.form['username'])     == 0
              and bool(request.form['email'])        == 0
              and bool(request.form['password'])     == 1
              and bool(request.form['new_password']) == 1
        ):
            password     = request.form['password']
            new_password = request.form['new_password']
            new_lang     = request.form['lang_sel'].upper()

            # Password form verification
            msg_err = form_password_check(password)

            if (msg_err is None):
                # Connect to database
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

                # Get user_details
                user_infos      = user_details(cursor, email, username)
                query_count_res = cursor.rowcount

                if (query_count_res > 0):

                    # Verify old password
                    hashed_pass = user_infos[3]
                    pass_verify = pwd_context.verify(password, hashed_pass)

                    if (bool(pass_verify == 1)):

                        # Encrypt new_password
                        new_password = pwd_context.encrypt(new_password)

                        user_upd_pass(cursor, new_password, username, email)

                        if (new_lang != lang.upper()):
                            user_upd_lang(cursor, new_lang, username, email)

                            if (lang == 'en'):
                                # Success
                                msg_suc = (
                                    'Password and language was successfully updated !'
                                )

                            else:
                                msg_suc = (
                                    'Le mot de passe et la langue '
                                    'ont été mis à jour avec succès !'
                                )

                                # Break connection
                                cursor.close()

                        else:
                            if (lang == 'en'):
                                # Success
                                msg_suc = 'Password was successfully updated !'

                            else:
                                msg_suc = (
                                    'Le mot de passe a été mis à jour '
                                    'avec succès !'
                                )

                            # Break connection
                            cursor.close()

                    else:
                        if (lang == 'en'):
                            msg_err = 'Old password is invalid !'
                        else:
                            msg_err = (
                                'L\'ancien mot de passe n\'est pas valide !'
                            )

                        cursor.close()

                else:
                    if (lang == 'en'):
                        msg_err = 'An error was occurred !'
                    else:
                        msg_err = 'Une erreur s\'est produite !'

                cursor.close()

        # Case 8 : Empty form
        elif (request.method == 'POST'
              and bool(request.form['username'])     == 0
              and bool(request.form['email'])        == 0
              and bool(request.form['password'])     == 0
              and bool(request.form['new_password']) == 0
        ):
            new_lang = request.form['lang_sel'].upper()

            if (new_lang != lang.upper()):
                user_upd_lang(cursor, new_lang, username, email)

                if (lang == 'en'):
                    # Success
                    msg_suc = 'The language was successfully updated !'

                else:
                    msg_suc = 'La langue a été mis à jour avec succès !'

                # Break connection
                cursor.close()

            else:
                if (lang == 'en'):
                    msg_err = (
                        'The selected language is identical to '
                        'the current language.'
                    )

                else:
                    msg_err = (
                        'La langue sélectionnée est identique à '
                        'la langue courante.'
                    )

                # Break connection
                cursor.close()

        return render_template(
            'users/settings.html',
            title        = 'EasyML - Settings',
            username     = username,
            email        = email,
            lang         = lang,
            nav_cat_name = navbar_cat_name,
            nav_cat_tag  = navbar_cat_tag,
            nav_cat_icon = navbar_cat_icon,
            nav_cat_lnk  = navbar_cat_link,
            nav_models   = navbar_models,
            nav_set_name = navbar_set_name,
            nav_set_icon = navbar_set_icon,
            nav_set_lnk  = navbar_set_link,
            msg_err      = msg_err,
            msg_suc      = msg_suc
        )

    else:
        return redirect('404')