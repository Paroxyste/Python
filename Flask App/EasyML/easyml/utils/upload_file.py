# -----------------------------------------------------------------------------

from easyml.utils.dataframe import df_html_show
from easyml.utils.dataframe import df_check_bin_val
from easyml.utils.dataframe import df_check_col_types
from easyml.utils.dataframe import df_col_count
from easyml.utils.dataframe import df_col_rename
from easyml.utils.dataframe import df_count_nan_val
from easyml.utils.dataframe import df_get_col_types
from easyml.utils.dataframe import df_numeric_cols
from easyml.utils.dataframe import load_dataframe

from easyml.utils.file      import allowed_extension
from easyml.utils.file      import file_check_size
from easyml.utils.file      import file_extension
from easyml.utils.file      import file_get_size
from easyml.utils.file      import file_tmp_path
from easyml.utils.file      import filename_encoder
from easyml.utils.file      import filename_get

from flask                  import request

import numpy as np
import os

# -----------------------------------------------------------------------------

def upload_file(lang, binary_check=False):

    # Init variables
    (data_to_html, df, msg_suc, msg_err, msg_warn) = (None,) * 5

    # Init list
    (choice_list, colname_list) = ([], ) * 2

    file = request.files['file']
    sep  = request.form['sep_select']

    # Get filename
    filename = filename_get(file)

    # Get file extension
    ext = file_extension(filename)

    # Check if extension was allowed
    msg_err = allowed_extension(ext, lang)

    if (msg_err is None):
        # Get tempory path
        path = file_tmp_path()

        # Save file for analysis
        file.save(os.path.join(path, filename))

        # Encode filename
        new_tmp_path = filename_encoder(path, filename, ext)

        # Check filesize
        file_size = file_get_size(new_tmp_path)
        msg_err   = file_check_size(file_size, new_tmp_path, lang)

        if (msg_err is None):
            # Load to dataframe
            df = load_dataframe(ext, new_tmp_path, sep)

            # Check num of columns
            msg_err = df_col_count(df, lang)

            if (msg_err is None):
                # Check if datas contain good coltypes for this model
                msg_err = df_check_col_types(df, [float, np.float64, int, np.int64], lang)

                if (msg_err is None):
                    # Check NaN values
                    msg_warn = df_count_nan_val(df, lang)

                    if (msg_warn != None):
                        # Delete missing values
                        df.dropna(inplace=True)

                    # Rename columns if str got space
                    df = df_col_rename(df)

                    # Get columns types
                    col_types = df_get_col_types(df)

                    # Get float columns
                    colname_list = df_numeric_cols(col_types)

                    # Select only needed columns
                    df = df[colname_list]

                    if (binary_check == True):
                        # Check that the dataset contains values less than or equal to 1
                        msg_err = df_check_bin_val(df, lang)

                        if (msg_err is None):
                            # Get choice list
                            choice_list = np.arange(1, len(df.columns) + 1)

                    # Show uploading files
                    data_to_html = df_html_show(df)

                    if (lang == 'en'):
                        msg_suc = (
                            'The data was successfully uploaded. '
                            'You can now visualize your data.'
                        )

                    else:
                        msg_suc = (
                            'Les données ont été téléchargées avec succès. '
                            'Vous pouvez maintenant visualiser vos données.'
                        )

    return [msg_err, msg_suc, msg_warn, 
            new_tmp_path, colname_list, 
            data_to_html, df,
            choice_list]