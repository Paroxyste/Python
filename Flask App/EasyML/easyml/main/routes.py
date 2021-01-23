from easyml._init_         import mysql

from easyml.utils.datas    import datas_cat_nav
from easyml.utils.datas    import datas_mod_nav
from easyml.utils.datas    import datas_set_nav

from easyml.utils.favorite import favorite_del
from easyml.utils.favorite import favorite_list

from easyml.utils.users    import user_details

from easyml.utils.cards    import cards_categories
from easyml.utils.cards    import cards_favorite

from flask                 import Blueprint
from flask                 import redirect
from flask                 import render_template
from flask                 import request
from flask                 import session
from flask                 import url_for

import MySQLdb.cursors

# -----------------------------------------------------------------------------
# Init main

main = Blueprint('main', __name__)

# -----------------------------------------------------------------------------
# Home / Root

@main.route('/', methods=['GET', 'POST'])
def home():
    # Check if user is loggedin
    if ('loggedin' in session):

        # Get session details
        username = session['username']
        email    = session['email']
        lang     = session['lang']

        # Define category tag
        cat_tag = 'HOME'

        # Connect to database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Get categories of navbar
        navbar_cat       = datas_cat_nav(cursor, lang)
        navbar_cat_name  = navbar_cat[0]
        navbar_cat_tag   = navbar_cat[1]
        navbar_cat_icon  = navbar_cat[2]
        navbar_cat_link  = navbar_cat[3]

        # Get models of navbar
        navbar_models = datas_mod_nav(cursor, lang, navbar_cat_tag)

        # Get settings of navbar
        navbar_settings = datas_set_nav(cursor, lang)
        navbar_set_name = navbar_settings[0]
        navbar_set_icon = navbar_settings[1]
        navbar_set_link = navbar_settings[2]

        # Get category details
        cat_details   = cards_categories(cursor, lang, cat_tag)
        cat_name      = cat_details[0]
        cat_link      = cat_details[3]

        # Get user ID
        user_infos = user_details(cursor, email, username)
        user_id    = user_infos[0]

        # Get favorite list
        favorite = favorite_list(cursor, user_id)

        # Have favorite cards
        if (len(favorite) > 0):

            # Get favorite card datas
            favorite_cards       = cards_favorite(cursor, lang, username, email)
            favorite_card_id     = favorite_cards[0]
            favorite_card_name   = favorite_cards[1]
            favorite_card_desc   = favorite_cards[2]
            favorite_card_link   = favorite_cards[3]
            favorite_card_img    = favorite_cards[4]

            # Remove favorite
            if (request.method == 'POST' 
                and bool(request.form['model_id']) == 1
            ):
                model_id = int(request.form['model_id'])

                # Favorite already existing -> remove favorite
                if (model_id in favorite):
                    favorite_del(cursor, user_id, model_id)

                    # Reload page
                    return redirect(url_for(cat_link))

            # Break connection
            cursor.close()

            return render_template(
                'main/dashboard.html',
                title        = cat_name,
                username     = username,
                lang         = lang,
                nav_cat_name = navbar_cat_name,
                nav_cat_tag  = navbar_cat_tag,
                nav_cat_icon = navbar_cat_icon,
                nav_cat_lnk  = navbar_cat_link,
                nav_models   = navbar_models,
                nav_set_name = navbar_set_name,
                nav_set_icon = navbar_set_icon,
                nav_set_lnk  = navbar_set_link,
                cat_tag      = cat_tag,
                card_id      = favorite_card_id,
                card_name    = favorite_card_name,
                card_desc    = favorite_card_desc,
                card_link    = favorite_card_link,
                card_image   = favorite_card_img,
                favorite     = favorite
            )

        else:
            # Break connection
            cursor.close()

            return render_template(
                'main/dashboard.html',
                title        = cat_name,
                username     = username,
                lang         = lang,
                nav_cat_name = navbar_cat_name,
                nav_cat_tag  = navbar_cat_tag,
                nav_cat_icon = navbar_cat_icon,
                nav_cat_lnk  = navbar_cat_link,
                nav_models   = navbar_models,
                nav_set_name = navbar_set_name,
                nav_set_icon = navbar_set_icon,
                nav_set_lnk  = navbar_set_link,
                cat_tag      = cat_tag,
                favorite     = favorite
            )

    else:
        return render_template(
            'home.html',
            title='Welcome to EasyML'
        )