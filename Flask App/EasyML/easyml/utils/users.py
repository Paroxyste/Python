from datetime      import datetime
from easyml._init_ import mysql
from flask         import session

# -----------------------------------------------------------------------------

def user_add(cursor, username, email, password, register_date, lang):
    msg_suc = None

    query = (
        'INSERT INTO users '
        'VALUES (NULL, %s, %s, %s, %s, %s, NULL);'
    )

    cursor.execute(query, (username, email, password, register_date, lang))

    # Commit to DB
    mysql.connection.commit()

    # Success
    msg_suc = 'You have successfully registered !'

    return msg_suc

# -----------------------------------------------------------------------------

def user_del_account(cursor, username, email, lang):
    msg_suc = None

    query = (
        'DELETE FROM users '
        'WHERE (username = %s AND email = %s);'
    )

    cursor.execute(query, (username, email))

    # Commit to DB
    mysql.connection.commit()

    if (lang == 'en'):
        # Account successfuly deleted
        msg_suc = 'Your account has been deleted !'

    else:
        msg_suc = 'Votre compte a été supprimé !'

    return msg_suc

# -----------------------------------------------------------------------------

def user_del_session():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('email'   , None)
    session.pop('lang'    , None)

# -----------------------------------------------------------------------------

def user_details(cursor, email, username):
    # Get user session values
    query = (
        'SELECT id, username, email, password, lang '
        'FROM users '
    )

    if (email == None):
        query += 'WHERE username = %s;'

        cursor.execute(query, (username,))

    elif (username == None):
        query += 'WHERE email = %s;'

        cursor.execute(query, (email,))

    else:
        query += 'WHERE (email = %s AND username = %s);'

        cursor.execute(query, (email, username))

    # Fetch query result
    query_result = cursor.fetchone()

    if (cursor.rowcount > 0):
        # Get user details
        elems = list(map(query_result.get, query_result))

    else:
        elems = []

    return elems

# -----------------------------------------------------------------------------

def user_register_date():
    register_date = datetime.now()
    register_date = register_date.strftime('%Y-%m-%d %H:%M:%S')

    return register_date

# -----------------------------------------------------------------------------

def user_upd_email(cursor, new_email, username, email):
    query = (
        'UPDATE users '
        'SET email = %s '
        'WHERE (username = %s AND email = %s);'
    )

    cursor.execute(query, (new_email, username, email))

    # Commit to DB
    mysql.connection.commit()

# -----------------------------------------------------------------------------

def user_upd_lang(cursor, new_lang, username, email):
    query = (
        'UPDATE users '
        'SET lang = %s '
        'WHERE (username = %s AND email = %s);'
    )

    cursor.execute(query, (new_lang, username, email))

    # Commit to DB
    mysql.connection.commit()

# -----------------------------------------------------------------------------

def user_upd_last_connection(cursor, username, email, date_now):
    query = (
        'UPDATE users '
        'SET last_connection = %s '
        'WHERE (username = %s AND email = %s);'
    )

    cursor.execute(query, (date_now, username, email))

    # Commit to DB
    mysql.connection.commit()

# -----------------------------------------------------------------------------

def user_upd_pass(cursor, new_password, username, email):
    query = (
        'UPDATE users '
        'SET password = %s '
        'WHERE (username = %s AND email = %s);'
    )

    cursor.execute(query, (new_password, username, email))

    # Commit to DB
    mysql.connection.commit()

# -----------------------------------------------------------------------------

def user_upd_username(cursor, new_username, username, email):
    query = (
        'UPDATE users '
        'SET username = %s '
        'WHERE (username = %s AND email = %s);'
    )

    cursor.execute(query, (new_username, username, email))

    # Commit to DB
    mysql.connection.commit()