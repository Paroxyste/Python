# -----------------------------------------------------------------------------

from easyml._init_ import mysql

# -----------------------------------------------------------------------------

def cards_categories(cursor, lang, tag):

    name = 'name_'        + lang + ', '
    desc = 'description_' + lang + ', '
    wiki = 'wiki_link_'   + lang

    query = (
        'SELECT ' + name + 'icon, ' + desc + 'link, ' + wiki + ' '
        'FROM categories '
        'WHERE tag = %s;'
    )

    cursor.execute(query, (tag,))

    # Fetch num of record and get query result
    query_result = cursor.fetchone()

    if (cursor.rowcount > 0):
        # Get categories cards elements
        cards = list(map(query_result.get, query_result))

    else:
        cards = []

    return cards

# -----------------------------------------------------------------------------

def cards_favorite(cursor, lang, username, email):

    name = 'mc.name_'        + lang + ', '
    desc = 'mc.description_' + lang + ', '

    query = (
        'SELECT mc.id, ' + name + desc + 'mc.link, mc.image '
        'FROM models_cat AS mc '
        'LEFT JOIN favorite AS f '
        'ON f.models_id = mc.id '
        'LEFT JOIN users AS u '
        'ON f.users_id = u.id '
        'WHERE (u.username = %s AND u.email = %s);'
    )

    cursor.execute(query, (username, email))

    # Fetch query result and list of columns used
    query_result   = cursor.fetchall()
    query_col_list = [c[0] for c in cursor.description]

    # Get models cards elements
    cards = cards_models_elems(query_result, query_col_list)

    return cards

# -----------------------------------------------------------------------------

def cards_models(cursor, lang, cat_tag):

    name = 'mc.name_'        + lang + ', '
    desc = 'mc.description_' + lang + ', '

    query = (
        'SELECT mc.id, ' + name + desc + 'mc.link, mc.image '
        'FROM models_cat AS mc '
        'LEFT JOIN categories AS c '
        'ON mc.id_categories = c.id '
        'WHERE c.tag = %s;'
    )

    cursor.execute(query, (cat_tag,))

    # Fetch query result and list of columns used
    query_result   = list(cursor.fetchall())
    query_col_list = [c[0] for c in cursor.description]

    # Get models cards elements
    cards = cards_models_elems(query_result, query_col_list)

    return cards

# -----------------------------------------------------------------------------

def cards_models_elems(query_result, query_col_list):

    elems = [list(map(lambda i: i[el], query_result)) for el in query_col_list]

    return elems