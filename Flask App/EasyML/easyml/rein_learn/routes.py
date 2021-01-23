# -----------------------------------------------------------------------------

from easyml._init_            import mysql

from easyml.utils.cards       import cards_categories
from easyml.utils.cards       import cards_models

from easyml.utils.dataframe   import df_html_show

from easyml.utils.datas       import datas_cat_nav
from easyml.utils.datas       import datas_mod_nav
from easyml.utils.datas       import datas_model
from easyml.utils.datas       import datas_set_nav

from easyml.utils.favorite    import favorite_add
from easyml.utils.favorite    import favorite_del
from easyml.utils.favorite    import favorite_list

from easyml.utils.file        import file_remove

from easyml.utils.users       import user_details

from easyml.utils.upload_file import upload_file

from flask                    import Blueprint
from flask                    import redirect
from flask                    import render_template
from flask                    import request
from flask                    import session
from flask                    import url_for

import math
import MySQLdb.cursors
import os
import random

# -----------------------------------------------------------------------------
# Init rf

rf = Blueprint('rf', __name__)

# -----------------------------------------------------------------------------
# Reinforcement Learning Cat

@rf.route('/rein_forc_learn_cat', methods=['GET', 'POST'])
def rein_forc_learn_cat():
    # Check if user is loggedin
    if ('loggedin' in session):

        # Get session details
        username = session['username']
        email    = session['email']
        lang     = session['lang']

        # Define category tag
        cat_tag = 'RL'

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

        # Get category details
        cat_details   = cards_categories(cursor, lang, cat_tag)
        cat_name      = cat_details[0]
        cat_icon      = cat_details[1]
        cat_desc      = cat_details[2]
        cat_link      = cat_details[3]
        cat_wiki_link = cat_details[4]

        # Get models card datas
        models_cards      = cards_models(cursor, lang, cat_tag)
        model_card_id     = models_cards[0]
        model_card_name   = models_cards[1]
        model_card_desc   = models_cards[2]
        model_card_link   = models_cards[3]
        model_card_img    = models_cards[4]

        # Get user ID
        user_infos = user_details(cursor, email, username)
        user_id    = user_infos[0]

        # Get favorite list
        favorite = favorite_list(cursor, user_id)

        # Add or remove favorite
        if (request.method == 'POST' 
            and bool(request.form['model_id']) == 1
        ):
            model_id = int(request.form['model_id'])

            # Case 1: Favorite already existing -> remove favorite
            if (model_id in favorite):
                favorite_del(cursor, user_id, model_id)

                # Reload page
                return redirect(url_for(cat_link, _anchor=model_id))

            # Case 2: Favorite doesn't exist -> add to favorite
            elif (model_id not in favorite):
                favorite_add(cursor, user_id, model_id)

                # Reload page
                return redirect(url_for(cat_link, _anchor=model_id))

        # Break connection
        cursor.close()

        return render_template(
            'common/model_category.html',
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
            cat_name     = cat_name,
            cat_tag      = cat_tag,
            cat_icon     = cat_icon,
            cat_desc     = cat_desc,
            cat_link     = cat_link,
            cat_wiki     = cat_wiki_link,
            card_id      = model_card_id,
            card_name    = model_card_name,
            card_desc    = model_card_desc,
            card_link    = model_card_link,
            card_image   = model_card_img,
            favorite     = favorite
        )

    else:
        return redirect('404')

# -----------------------------------------------------------------------------
# Upper Confidence Bound (UCB)

@rf.route('/upper_confidence_bound', methods=['GET', 'POST'])
def upper_confidence_bound():
    # Check if user is loggedin
    if ('loggedin' in session):

        # Init variables
        (data_to_html, choice, graph_title, choice_select,
         msg_suc, msg_err, msg_warn) = (None,) * 7

        # Init integer
        total_reward = 0

        # Init list
        (choice_list, selected) = ([], ) * 2

        # Get session details
        username = session['username']
        lang     = session['lang']

        # Define tag category + model
        cat_tag = 'RL'
        mod_tag = 'UCB'

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

        # Get category details for breadcrumb
        cat_details   = cards_categories(cursor, lang, cat_tag)
        cat_name      = cat_details[0]
        cat_link      = cat_details[3]

        # Get model details for breadcrumb
        model_details = datas_model(cursor, lang, mod_tag)
        model_name    = model_details[0]
        model_link    = model_details[1]

        # Break connection
        cursor.close()

        if (request.method == 'POST'):

            # Upload file
            if (request.form['submit_btn'] == 'Upload Now'
                or request.form['submit_btn'] == 'Envoyer maintenant'):

                # All fields was complete
                if (bool(request.files['file']) == 1 
                    and bool(request.form['sep_select']) == 1
                ):
                    get_upload_datas = upload_file(lang, True)
                    msg_err          = get_upload_datas[0]
                    msg_suc          = get_upload_datas[1]
                    msg_warn         = get_upload_datas[2]

                    global new_tmp_path
                    new_tmp_path = get_upload_datas[3]

                    data_to_html = get_upload_datas[5]

                    global df
                    df = get_upload_datas[6]

                    choice_list = get_upload_datas[7]

                else:
                    if (lang == 'en'):
                        # Submit without upload file
                        msg_err = (
                            'Please upload your data and select a separator.'
                        )

                    else:
                        msg_err = (
                            'Veuillez télécharger vos données et choisir'
                            ' un séparateur.'
                        )

            # Model compute
            if (request.form['submit_btn'] == 'Launch the model'
                or request.form['submit_btn'] == 'Lancer le modèle'):
                choice_select = int(request.form['choice'])

                # Show uploading files
                data_to_html = df_html_show(df)

                num_of_select  = [0] * choice_select
                sum_of_rewards = [0] * choice_select

                for n in range(len(df)):
                    choice = 0
                    max_upper_bound = 0

                    for i in range(choice_select):

                        if (num_of_select[i] > 0):
                            avg_reward = sum_of_rewards[i] / num_of_select[i]
                            delta_i    = math.sqrt(1.5 * math.log(n + 1) / num_of_select[i])

                            upper_bound = avg_reward + delta_i

                        else:
                            upper_bound = math.inf

                        if (upper_bound > max_upper_bound):
                            choice = i
                            max_upper_bound = upper_bound

                    selected.append(choice)

                    num_of_select[choice] += 1

                    reward = df.values[n, choice]

                    sum_of_rewards[choice] += reward

                    total_reward += reward

                if (lang == 'en'):
                    # Add graph title
                    graph_title = (
                        'Histogram of selection for ' 
                        + str(choice_select) + 
                        ' choices :'
                    )

                    # Success
                    msg_suc = (
                        'The model was successfully calculated. '
                        'Your data was automatically deleted.'
                    )
                    
                else:
                    graph_title = (
                        'Histogramme de sélection pour '
                        + str(choice_select) +
                        ' choix :'
                    )

                    msg_suc = (
                        'Le modèle a été calculé avec succès. '
                        'Vos données ont été automatiquement supprimées.'
                    )

                # Delete file
                file_remove(new_tmp_path)

        return render_template(
            'rein_learn/upper_conf_bound.html',
            title        = model_name,
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
            cat_name     = cat_name,
            cat_tag      = cat_tag,
            cat_link     = cat_link,
            model_name   = model_name,
            model_link   = model_link,
            msg_err      = msg_err,
            msg_suc      = msg_suc,
            msg_warn     = msg_warn,
            data_show    = data_to_html,
            choice_list  = choice_list,
            choice       = choice,
            choice_sel   = choice_select,
            total_reward = total_reward,
            res_selected = selected, 
            graph_title  = graph_title
        )

    else:
        return redirect('404')

# -----------------------------------------------------------------------------
# Thompson Sampling

@rf.route('/thompson_sampling', methods=['GET', 'POST'])
def thompson_sampling():
    # Check if user is loggedin
    if ('loggedin' in session):

        # Init variables
        (data_to_html, choice, graph_title, choice_select,
         msg_suc, msg_err, msg_warn) = (None,) * 7

        # Init integer
        total_reward = 0

        # Init list
        (choice_list, selected) = ([], ) * 2

        # Get session details
        username = session['username']
        lang     = session['lang']

        # Define tag category + model
        cat_tag = 'RL'
        mod_tag = 'TS'

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

        # Get category details for breadcrumb
        cat_details   = cards_categories(cursor, lang, cat_tag)
        cat_name      = cat_details[0]
        cat_link      = cat_details[3]

        # Get model details for breadcrumb
        model_details = datas_model(cursor, lang, mod_tag)
        model_name    = model_details[0]
        model_link    = model_details[1]

        # Break connection
        cursor.close()

        if (request.method == 'POST'):

            # Upload file
            if (request.form['submit_btn'] == 'Upload Now'
                or request.form['submit_btn'] == 'Envoyer maintenant'):

                # All fields was complete
                if (bool(request.files['file']) == 1 
                    and bool(request.form['sep_select']) == 1
                ):
                    get_upload_datas = upload_file(lang, True)
                    msg_err          = get_upload_datas[0]
                    msg_suc          = get_upload_datas[1]
                    msg_warn         = get_upload_datas[2]

                    global new_tmp_path
                    new_tmp_path = get_upload_datas[3]

                    data_to_html = get_upload_datas[5]

                    global df
                    df = get_upload_datas[6]

                    choice_list = get_upload_datas[7]

                else:
                    if (lang == 'en'):
                        # Submit without upload file
                        msg_err = (
                            'Please upload your data and select a separator.'
                        )

                    else:
                        msg_err = (
                            'Veuillez télécharger vos données et choisir'
                            ' un séparateur.'
                        )

            # Model compute
            if (request.form['submit_btn'] == 'Launch the model'
                or request.form['submit_btn'] == 'Lancer le modèle'):
                choice_select = int(request.form['choice'])

                # Show uploading files
                data_to_html = df_html_show(df)

                num_of_rewards_1 = [0] * choice_select
                num_of_rewards_0 = [0] * choice_select

                for n in range(len(df)):
                    choice = 0
                    max_random = 0

                    for i in range(choice_select):
                        random_beta = random.betavariate(
                            num_of_rewards_1[i] + 1, 
                            num_of_rewards_0[i] + 1
                        )
                            
                        if (random_beta > max_random):
                            choice = i
                            max_random = random_beta

                    selected.append(choice)
                    reward = df.values[n, choice]

                    if (reward == 1):
                        num_of_rewards_1[choice] += 1

                    else:
                        num_of_rewards_0[choice] += reward

                    total_reward += reward

                if (lang == 'en'):
                    # Add graph title
                    graph_title = (
                        'Histogram of selection for ' 
                        + str(choice_select) + 
                        ' choices :'
                    )

                    # Success
                    msg_suc = (
                        'The model was successfully calculated. '
                        'Your data was automatically deleted.'
                    )
                    
                else:
                    graph_title = (
                        'Histogramme de sélection pour '
                        + str(choice_select) +
                        ' choix :'
                    )

                    msg_suc = (
                        'Le modèle a été calculé avec succès. '
                        'Vos données ont été automatiquement supprimées.'
                    )

                # Delete file
                file_remove(new_tmp_path)

        return render_template(
            'rein_learn/thomp_samp.html',
            title        = model_name,
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
            cat_name     = cat_name,
            cat_tag      = cat_tag,
            cat_link     = cat_link,
            model_name   = model_name,
            model_link   = model_link,
            msg_err      = msg_err,
            msg_suc      = msg_suc,
            msg_warn     = msg_warn,
            data_show    = data_to_html,
            choice_list  = choice_list,
            choice       = choice,
            choice_sel   = choice_select,
            total_reward = total_reward,
            res_selected = selected, 
            graph_title  = graph_title
        )

    else:
        return redirect('404')