# -----------------------------------------------------------------------------

from easyml._init_ import mysql

# -----------------------------------------------------------------------------

def favorite_add(cursor, user_id, model_card_id):
    query = (
        'INSERT INTO favorite '
        'VALUES (NULL, %s, %s);'
    )

    cursor.execute(query, (user_id, model_card_id))

    # Commit to DB
    mysql.connection.commit()

# -----------------------------------------------------------------------------

def favorite_del(cursor, user_id, favorite_card_id):
    query = (
        'DELETE FROM favorite '
        'WHERE (users_id = %s AND models_id = %s);'
    )

    cursor.execute(query, (user_id, favorite_card_id))

    # Commit to DB
    mysql.connection.commit()

# -----------------------------------------------------------------------------

def favorite_list(cursor, user_id):
    query = (
        'SELECT f.models_id '
        'FROM favorite AS f '
        'LEFT JOIN users AS u '
        'ON f.users_id = u.id '
        'WHERE u.id = %s;'
    )

    cursor.execute(query, (user_id,))

    # Fetch query result
    query_result = cursor.fetchall()

    # Get favorite list
    favorite = [id['models_id'] for id in query_result]

    return favorite