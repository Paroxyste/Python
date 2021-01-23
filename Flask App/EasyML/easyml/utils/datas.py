def datas_cat_nav(cursor, lang):

    name = 'name_' + lang + ', '

    query = (
        'SELECT ' + name + 'tag, icon, link '
        'FROM categories '
    )

    cursor.execute(query)

    # Fetch query result and list of columns used
    query_result   = cursor.fetchall()
    query_col_list = [c[0] for c in cursor.description]

    # Get categories name, tag, icon, link for navigation
    elems = datas_nav_elem(query_result, query_col_list)

    return elems

# -----------------------------------------------------------------------------

def datas_model(cursor, lang, tag_model):

    name = 'name_' + lang + ', '

    query = (
        'SELECT ' + name + 'link '
        'FROM models_cat '
        'WHERE tag = %s; '
    )

    cursor.execute(query, (tag_model,))

    # Fetch query result
    query_result = cursor.fetchone()


    if (cursor.rowcount > 0):
        # Get models name, link
        elems = list(map(query_result.get, query_result))

    else:
        elems = []

    return elems

# -----------------------------------------------------------------------------

def datas_mod_nav(cursor, lang, navbar_cat_tag):

    elems_list = []

    name = 'mc.name_' + lang + ', '

    for nav_cat in navbar_cat_tag:

        query = (
            'SELECT ' + name + 'mc.link '
            'FROM models_cat AS mc '
            'LEFT JOIN categories AS c '
            'ON mc.id_categories = c.id '
            'WHERE c.tag = %s;'
        )

        cursor.execute(query, (nav_cat,))

        # Fetch query result 
        query_result = cursor.fetchall()

        # Get models names and links for navigation
        elems = [list(el.values()) for el in query_result]
        elems_list.append(elems)

    elems_list[0] = []

    return elems_list

# -----------------------------------------------------------------------------

def datas_nav_elem(query_result, query_col_list):
    elems = [list(map(lambda i: i[el], query_result)) for el in query_col_list]

    return elems

# -----------------------------------------------------------------------------

def datas_set_nav(cursor, lang):
    query = (
        'SELECT name_' + lang + ', icon, link '
        'FROM settings '
    )

    cursor.execute(query)

    # Fetch query result and list of columns used
    query_result   = cursor.fetchall()
    query_col_list = [c[0] for c in cursor.description]

    # Get settings name, icon, link
    elems = datas_nav_elem(query_result, query_col_list)

    return elems