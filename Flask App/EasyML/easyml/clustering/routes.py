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

from kneed                    import KneeLocator

from scipy.cluster.hierarchy  import fcluster
from scipy.cluster.hierarchy  import linkage

from sklearn.cluster          import AgglomerativeClustering
from sklearn.cluster          import KMeans

import MySQLdb.cursors
import numpy as np
import os
import statistics

# -----------------------------------------------------------------------------
# Init clust

clust = Blueprint('clust', __name__)

# -----------------------------------------------------------------------------
# Clustering Category

@clust.route('/clustering_category', methods=['GET', 'POST'])
def clustering_category():
    # Check if user is loggedin
    if ('loggedin' in session):

        # Get session details
        username = session['username']
        email    = session['email']
        lang     = session['lang']

        # Define category tag
        cat_tag = 'CLU'

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
# K-Means Clustering

@clust.route('/k_means_clustering', methods=['GET', 'POST'])
def k_means_clustering():
    # Check if user is loggedin
    if ('loggedin' in session):

        # Init variables
        (data_to_html, graph_title, k,
         msg_suc, msg_err, msg_warn, X_col, Y_col) = (None,) * 8

        # Init list
        (cluster_pts, columns) = ([], ) * 2

        # Get session details
        username = session['username']
        lang     = session['lang']

        # Define tag category + model
        cat_tag = 'CLU'
        mod_tag = 'KMC'

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
                    get_upload_datas = upload_file(lang, False)
                    msg_err          = get_upload_datas[0]
                    msg_suc          = get_upload_datas[1]
                    msg_warn         = get_upload_datas[2]

                    global new_tmp_path
                    new_tmp_path = get_upload_datas[3]

                    global colname_list
                    colname_list = get_upload_datas[4]
                    columns      = colname_list

                    data_to_html = get_upload_datas[5]

                    global df
                    df = get_upload_datas[6]

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
                X_col = request.form['X_col']
                Y_col = request.form['Y_col']

                # Get colname list
                columns = colname_list

                # Show uploading files
                data_to_html = df_html_show(df)

                if (X_col == Y_col):

                    if (lang == 'en'):
                        msg_err = 'X_col and Y_col must be different.'
                    else:
                        msg_err = 'X_col et Y_col doivent être différents.'

                if (msg_err is None):
                    # Delete feature from columns
                    [columns.remove(col) for col in [X_col, Y_col]]

                    X = df.loc[:, [X_col, Y_col]].values

                    # Use elbow method to find the optimal number of clusters
                    cluster   = []
                    n_cluster = np.arange(1, 21)

                    for i in n_cluster:
                        kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
                        kmeans.fit(X)

                        cluster.append(kmeans.inertia_)

                    kl = KneeLocator(n_cluster, cluster, curve='convex', direction='decreasing')

                    # Get the best number of clusters
                    k = kl.elbow

                    # Training K-Means model
                    kmeans   = KMeans(n_clusters=k, init='k-means++', random_state=42)
                    y_kmeans = kmeans.fit_predict(X)

                    # Get plot pts
                    [cluster_pts.append([X[y_kmeans == i, 0].tolist(), X[y_kmeans == i, 1].tolist()]) for i in np.arange(k)]

                    if (lang == 'en'):
                        # Add graph title
                        graph_title = str(k) + ' clusters have been defined :'

                        # Success
                        msg_suc = (
                            'The model was successfully calculated. '
                            'Your data was automatically deleted.'
                        )
                    
                    else:
                        graph_title = str(k) + ' groupes ont été définis :'

                        msg_suc = (
                            'Le modèle a été calculé avec succès.  '
                            'Vos données ont été automatiquement supprimées.'
                        )

                    # Delete file
                    file_remove(new_tmp_path)

        return render_template(
            'clustering/k_mean_clust.html',
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
            df_columns   = columns,
            X_col        = X_col,
            Y_col        = Y_col,
            k            = k,
            cluster_pts  = cluster_pts,
            graph_title  = graph_title
        )

    else:
        return redirect('404')

# -----------------------------------------------------------------------------
# Hierarchical Clustering

@clust.route('/hierarchical_clustering', methods=['GET', 'POST'])
def hierarchical_clustering():
    # Check if user is loggedin
    if ('loggedin' in session):

        # Init variables
        (data_to_html, graph_title, k,
         msg_suc, msg_err, msg_warn, X_col, Y_col) = (None,) * 8

        # Init list
        (cluster_pts, columns) = ([], ) * 2

        # Get session details
        username = session['username']
        lang     = session['lang']

        # Define tag category + model
        cat_tag = 'CLU'
        mod_tag = 'HC'

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
                    get_upload_datas = upload_file(lang, False)
                    msg_err          = get_upload_datas[0]
                    msg_suc          = get_upload_datas[1]
                    msg_warn         = get_upload_datas[2]

                    global new_tmp_path
                    new_tmp_path = get_upload_datas[3]

                    global colname_list
                    colname_list = get_upload_datas[4]
                    columns      = colname_list

                    data_to_html = get_upload_datas[5]

                    global df
                    df = get_upload_datas[6]

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
                X_col = request.form['X_col']
                Y_col = request.form['Y_col']

                # Get colname list
                columns = colname_list

                # Show uploading files
                data_to_html = df_html_show(df)

                if (X_col == Y_col):

                    if (lang == 'en'):
                        msg_err = 'X_col and Y_col must be different.'
                    else:
                        msg_err = 'X_col et Y_col doivent être différents.'

                if (msg_err is None):
                    # Delete feature from columns
                    [columns.remove(col) for col in [X_col, Y_col]]

                    X = df.loc[:, [X_col, Y_col]].values

                    # Use the dendrogram to find the optimal number of clusters
                    dist = linkage(X, 'ward')

                    # N cluster @ 50%
                    line_cut = statistics.mean([dist.min(), dist.max()])

                    # Get the best number of clusters
                    k = fcluster(dist, t=line_cut, criterion='distance').max()

                    # Training K-Means model
                    hc = AgglomerativeClustering(n_clusters=k, affinity='euclidean', linkage='ward')
                    y_hc = hc.fit_predict(X)

                    # Get plot pts
                    [cluster_pts.append([X[y_hc == i, 0].tolist(), X[y_hc == i, 1].tolist()]) for i in np.arange(k)]

                    if (lang == 'en'):
                        # Add graph title
                        graph_title = str(k) + ' clusters have been defined :'

                        # Success
                        msg_suc = (
                            'The model was successfully calculated. '
                            'Your data was automatically deleted.'
                        )
                    
                    else:
                        graph_title = str(k) + ' groupes ont été définis :'

                        msg_suc = (
                            'Le modèle a été calculé avec succès.  '
                            'Vos données ont été automatiquement supprimées.'
                        )

                    # Delete file
                    file_remove(new_tmp_path)

        return render_template(
            'clustering/hier_clust.html',
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
            df_columns   = columns,
            X_col        = X_col,
            Y_col        = Y_col,
            k            = k,
            cluster_pts  = cluster_pts,
            graph_title  = graph_title
        )

    else:
        return redirect('404')
