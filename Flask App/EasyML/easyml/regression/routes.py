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

from sklearn                  import linear_model
from sklearn.linear_model     import LinearRegression
from sklearn.metrics          import mean_squared_error
from sklearn.metrics          import r2_score
from sklearn.model_selection  import train_test_split
from sklearn.preprocessing    import PolynomialFeatures

import math
import MySQLdb.cursors
import numpy as np
import os
import statistics

# -----------------------------------------------------------------------------
# Init reg

reg = Blueprint('reg', __name__)

# -----------------------------------------------------------------------------
# Regression Category

@reg.route('/regression_category', methods=['GET', 'POST'])
def regression_category():
    # Check if user is loggedin
    if ('loggedin' in session):

        # Get session details
        username = session['username']
        email    = session['email']
        lang     = session['lang']

        # Define category tag
        cat_tag = 'REG'

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

            # Favorite already existing -> remove favorite
            if (model_id in favorite):
                favorite_del(cursor, user_id, model_id)

                # Reload page
                return redirect(url_for(cat_link, _anchor=model_id))

            # Add to favorite
            else :
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
            card_image   = model_card_img,
            card_name    = model_card_name,
            card_desc    = model_card_desc,
            card_link    = model_card_link,
            favorite     = favorite
        )

    else:
        return redirect('404')

# -----------------------------------------------------------------------------
# Simple Linear Regression

@reg.route('/simple_linear_regression', methods=['GET', 'POST'])
def simple_linear_regression():
    # Check if user is loggedin
    if ('loggedin' in session):

        # Init variables
        (data_to_html, feature, graph_title, 
         msg_suc, msg_err, msg_warn) = (None,) * 6

        # Init list
        (columns, score_list) = ([], ) * 2

        # Get session details
        username = session['username']
        lang     = session['lang']

        # Define tag category + model
        cat_tag = 'REG'
        mod_tag = 'SLR'

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

                    print(msg_err)
                    print(msg_suc)
                    print(msg_warn)

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
                            'Veuillez télécharger vos données et '
                            'choisir un séparateur.'
                        )

            # Model compute
            if (request.form['submit_btn'] == 'Launch the model'
                or request.form['submit_btn'] == 'Lancer le modèle'):
                feature = request.form['feature']

                # Show uploading files
                data_to_html = df_html_show(df)

                # Get colname list
                columns = colname_list

                # Delete feature from columns
                columns.remove(feature)

                for i in columns:
                    x_feat = df[feature].values.reshape(-1, 1)
                    y_targ = df[i].values.reshape(-1, 1)

                    # Train Test
                    X_train, X_test, y_train, y_test = train_test_split(
                        x_feat,
                        y_targ,
                        test_size=0.33,
                        random_state=42
                    )

                    # Create model and fit
                    regressor = LinearRegression().fit(X_train, y_train)

                    # Predicting test set results
                    y_test_pred = regressor.predict(X_test)

                    # Prediction
                    y_pred = regressor.predict(X_train)
                    y_pred = y_pred.tolist()

                    # Accuracy
                    r2_test  = r2_score(y_test , y_test_pred) * 100
                    r2_train = r2_score(y_train, y_pred) * 100

                    score_list.append(round(statistics.mean([r2_test, r2_train]), 2))

                if (lang == 'en'):
                    # Add graph title
                    graph_title = (
                        'Comparison of the correlation between ' + feature + 
                        ' and the columns :'
                    )

                    # Success
                    msg_suc = (
                        'The model was successfully calculated. '
                        'Your data was automatically deleted.'
                    )

                else:
                    graph_title = (
                        'Comparaison de la corrélation entre ' + feature + 
                        ' et les colonnes :'
                    )

                    msg_suc = (
                        'Le modèle a été calculé avec succès.  '
                        'Vos données ont été automatiquement supprimées.'
                    )

                # Delete file
                file_remove(new_tmp_path)

        return render_template(
            'regression/simp_lin_reg.html',
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
            feature      = feature,
            score_list   = score_list,
            graph_title  = graph_title
        )

    else:
        return redirect('404')

# -----------------------------------------------------------------------------
# Multiple Linear Regression

@reg.route('/multiple_linear_regression', methods=['GET', 'POST'])
def multiple_linear_regression():
    # Check if user is loggedin
    if ('loggedin' in session):

        # Init variables
        (data_to_html, X_col, Y_col, graph_title, 
         msg_suc, msg_err, msg_warn) = (None,) * 7

        # Init list
        (columns, score_list) = ([], ) * 2

        # Get session details
        username = session['username']
        lang     = session['lang']

        # Define tag category + model
        cat_tag = 'REG'
        mod_tag = 'MLR'

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
                            'Veuillez télécharger vos données et '
                            'choisir un séparateur.'
                        )

            # Model compute
            if (request.form['submit_btn'] == 'Launch the model'
                or request.form['submit_btn'] == 'Lancer le modèle'):
                X_col = request.form['X_col']
                Y_col = request.form['Y_col']

                # Show uploading files
                data_to_html = df_html_show(df)

                # Get colname list
                columns = colname_list

                # Delete feature from columns
                columns.remove(X_col)
                columns.remove(Y_col)

                for i in columns:
                    x_feat = df[[X_col, i]].values
                    y_targ = df[Y_col].values

                    # Train Test
                    X_train, X_test, y_train, y_test = train_test_split(
                        x_feat,
                        y_targ,
                        test_size=0.33,
                        random_state=42
                    )

                    # Create model and fit
                    regressor = LinearRegression().fit(X_train, y_train)

                    # Predicting test set results
                    y_test_pred = regressor.predict(X_test)

                    # Prediction
                    y_pred = regressor.predict(X_train)
                    y_pred = y_pred.tolist()

                    # Accuracy
                    r2_test  = r2_score(y_test , y_test_pred) * 100
                    r2_train = r2_score(y_train, y_pred) * 100

                    score_list.append(round(statistics.mean([r2_test, r2_train]), 2))

                columns = [X_col + ' + ' + c for c in columns]

                if (lang == 'en'):
                    # Add graph title
                    graph_title = (
                        'Comparison of the correlation between ' + Y_col + 
                        ' and the columns :'
                    )

                    # Success
                    msg_suc = (
                        'The model was successfully calculated. '
                        'Your data was automatically deleted.'
                    )

                else:
                    graph_title = (
                        'Comparaison de la corrélation entre ' + Y_col + 
                        ' et les colonnes :'
                    )

                    msg_suc = (
                        'Le modèle a été calculé avec succès.  '
                        'Vos données ont été automatiquement supprimées.'
                    )

                # Delete file
                file_remove(new_tmp_path)

        return render_template(
            'regression/mul_lin_reg.html',
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
            score_list   = score_list,
            graph_title  = graph_title
        )

    else:
        return redirect('404')

# -----------------------------------------------------------------------------
# Polynomial Regression

@reg.route('/polynomial_regression', methods=['GET', 'POST'])
def polynomial_regression():
    # Check if user is loggedin
    if ('loggedin' in session):

        # Init variables
        (data_to_html, feature, graph_title, 
         msg_suc, msg_err, msg_warn) = (None,) * 6

        # Init list
        (columns, res_list, score_list) = ([], ) * 3

        # Get session details
        username = session['username']
        lang     = session['lang']

        # Define tag category + model
        cat_tag = 'REG'
        mod_tag = 'PR'

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
                            'Veuillez télécharger vos données et '
                            'choisir un séparateur.'
                        )

            # Model compute
            if (request.form['submit_btn'] == 'Launch the model'
                or request.form['submit_btn'] == 'Lancer le modèle'):
                feature = request.form['feature']

                # Get colname list
                columns = colname_list

                # Show uploading files
                data_to_html = df_html_show(df)

                # Delete feature from columns
                columns.remove(feature)

                for i in columns:
                    x_feat = df[feature].values.reshape(-1, 1)
                    y_targ = df[i].values.reshape(-1, 1)

                    # Train Test
                    X_train, X_test, y_train, y_test = train_test_split(
                        x_feat,
                        y_targ,
                        test_size=0.33,
                        random_state=42
                    )

                    score_rmse = []
                    min_rmse, min_deg = (math.inf,) * 2

                    for deg in range(1, 11):

                        # Train features
                        poly_features = PolynomialFeatures(degree=deg, include_bias=False)
                        x_poly_train  = poly_features.fit_transform(X_train)

                        # Linear regression
                        poly_reg = LinearRegression().fit(x_poly_train, y_train)

                        # Compare with test data
                        x_poly_test  = poly_features.fit_transform(X_test)
                        poly_predict = poly_reg.predict(x_poly_test)

                        poly_rmse = np.sqrt(mean_squared_error(y_test, poly_predict))

                        score_rmse.append(poly_rmse)

                        # Cross-validation of degree
                        if (min_rmse > poly_rmse):
                            min_rmse = poly_rmse
                            min_deg  = deg

                    # Create Polynomial model
                    polynomial = PolynomialFeatures(degree=min_deg)

                    # Fit polynomial model
                    X_train = polynomial.fit_transform(X_train)
                    X_test  = polynomial.fit_transform(X_test)

                    # Create linear model and fit
                    regressor = linear_model.LinearRegression().fit(X_train, y_train)

                    # Predicting test set results
                    y_test_pred = regressor.predict(X_test)

                    # Prediction
                    y_pred = regressor.predict(X_train)
                    y_pred = y_pred.tolist()

                    # Accuracy
                    r2_test  = r2_score(y_test , y_test_pred) * 100
                    r2_train = r2_score(y_train, y_pred) * 100

                    res = [i, round(statistics.mean([r2_test, r2_train]), 2)]
                    res_list.append(res)

                # Save scoring
                score_list = [score[1] for score in res_list]

                if (lang == 'en'):
                    # Add graph title
                    graph_title = (
                        'Comparison of the correlation between ' + feature + 
                        ' and the columns :'
                    )

                    # Success
                    msg_suc = (
                        'The model was successfully calculated. '
                        'Your data was automatically deleted.'
                    )

                else:
                    graph_title = (
                        'Comparaison de la corrélation entre ' + feature + 
                        ' et les colonnes :'
                    )

                    msg_suc = (
                        'Le modèle a été calculé avec succès.  '
                        'Vos données ont été automatiquement supprimées.'
                    )

                # Delete file
                file_remove(new_tmp_path)

        return render_template(
            'regression/pol_reg.html',
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
            feature      = feature,
            score_list   = score_list,
            graph_title  = graph_title
        )

    else:
        return redirect('404')
