# -----------------------------------------------------------------------------

from easyml._init_            import mysql

from easyml.utils.cards       import cards_categories

from easyml.utils.datas       import datas_cat_nav
from easyml.utils.datas       import datas_mod_nav
from easyml.utils.datas       import datas_set_nav

from easyml.utils.file        import file_remove

from easyml.utils.upload_file import upload_file

from flask                    import Blueprint
from flask                    import redirect
from flask                    import render_template
from flask                    import request
from flask                    import session

from pandas_profiling         import ProfileReport

import hashlib
import MySQLdb.cursors
import os
import random
import string

# -----------------------------------------------------------------------------
# Init exp

exp = Blueprint('exp', __name__)

# -----------------------------------------------------------------------------
# Exploratory Analysis

@exp.route('/exploratory_analysis', methods=['GET', 'POST'])
def exploratory_analysis():
    # Check if user is loggedin
    if ('loggedin' in session):

        # Init variables
        (html_dl_link, msg_suc, msg_err, report) = (None,) * 4

        # Get session details
        username = session['username']
        lang     = session['lang']

        # Define tag category
        cat_tag = 'AE'

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
                    new_tmp_path     = get_upload_datas[3]
                    df               = get_upload_datas[6]

                    # Generate Analysis
                    save = ProfileReport(df, minimal=True)

                    # Save Report
                    os_path = 'C:/Users/Administrateur/Documents/EasyML/easyml/'
                    dir_path = 'static/dl/'

                    random_str = string.ascii_lowercase + string.digits
                    random_str = ''.join(random.sample(random_str, 16))

                    encode_name = hashlib.md5('exploratory_analysis'.encode())
                    encode_name = encode_name.hexdigest() + random_str + '.html'

                    html_dir_path = os_path + dir_path + encode_name
                    html_dl_link  = dir_path + encode_name

                    save.to_file(html_dir_path)

                    report  = True

                    if (lang == 'en'):
                        msg_suc = (
                            'The report was successfully generated. '
                            'The data was automatically deleted.'
                        )
                    
                    else:
                        msg_suc = (
                            'Le rapport a été produit avec succès. '
                            'Les données ont été automatiquement supprimées.'
                        )

                    # Delete file
                    file_remove(new_tmp_path)

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

        return render_template(
            'exploratory/exp_analysis.html',
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
            cat_link     = cat_link,
            msg_err      = msg_err,
            msg_suc      = msg_suc,
            report       = report,
            data_show    = html_dl_link
        )

    else:
        return redirect('404')