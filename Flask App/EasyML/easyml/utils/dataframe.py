# -----------------------------------------------------------------------------

from IPython.display import HTML

import pandas as pd

# -----------------------------------------------------------------------------

def df_check_col_types(df, col_type, lang):
    msg_err = None

    if (len(df.select_dtypes(col_type).columns) < 2):

        if (lang == 'en'):
            msg_err = 'The type of data is not adapted to this model.'
        
        else:
            msg_err = 'Le type de données n\'est pas adapté à ce modèle.'

    return msg_err

# -----------------------------------------------------------------------------

def df_check_bin_val(df, lang):
    msg_err = None

    values = [list(set(df[c].values)) for c in df.columns]
    values = list(set([x for l in values for x in l]))

    if (all(i <= 1.0 for i in values) == False):

        if (lang == 'en'):
            msg_err = 'The dataset contains values greater than 0 or 1.'

        else:
            msg_err = (
                'Le jeu de données contient des valeurs supérieures à 0 ou 1.'
            )

    return msg_err

# -----------------------------------------------------------------------------

def df_col_count(df, lang):
    msg_err = None

    if (len(df.columns) < 2):

        if (lang == 'en'):
            msg_err = (
                'The chosen separator is invalid '
                'or the data does not have enough columns.'
            )

        else:
            msg_err = (
                'Le séparateur choisi n\'est pas valide ou les données '
                'n\'ont pas assez de colonnes.'
            )

    return msg_err

# -----------------------------------------------------------------------------

def df_col_rename(df):
    df.columns = [c.replace(' ', '_') for c in df.columns]

    return df

# -----------------------------------------------------------------------------

def df_convert_cols(df, list_to_convert, new_type):
    # Convert all list elements
    for i in list_to_convert:
        df[i] = df[i].astype(new_type)

    return df

# -----------------------------------------------------------------------------

def df_count_nan_val(df, lang):
    msg_warn  = None
    nan_count = df.isna().sum().sum()

    if(nan_count > 0):

        if (lang == 'en'):
            msg_warn = (
                str(nan_count) + ' missing values detected. '
                'Rows containing missing values were automatically removed.'
            )

        else:
            msg_warn = (
                str(nan_count) + ' valeurs manquantes détectées. '
                'Les lignes contenant des valeurs manquantes ont été '
                'automatiquement supprimées.'
            )

    return msg_warn

# -----------------------------------------------------------------------------

def df_get_col_types(df):
    # Get column types
    col_types = list(df.dtypes.items())

    return col_types

# -----------------------------------------------------------------------------

def df_html_show(df):
    # Make bootsrap classes
    data_show = df.to_html(
        classes=[
            'display', 'table', 'nowrap', 'table-striped', 
            'table-hover', 'dataTable'
        ],
        max_rows=99, 
        notebook=True, 
        index=True,
    )

    # Hidden border
    data_show = data_show.replace(
        'border="1"', 
        (
            'border="0" id="zero-configuration" role="grid" '
            'aria-describedby="zero-configuration_info"'
        )
    )

    # Center results
    data_show = data_show.replace('style="text-align: right;"', '')
    data_show = data_show.replace('<td>', '<td class="text-center">')
    data_show = data_show.replace('<th>', '<th class="text-center">')

    # Transform to HTML
    data_show = HTML(data_show)

    return data_show

# -----------------------------------------------------------------------------

def df_object_cols(col_types):
    col_object  = []

    # col[0] = colname, col[1] = dtypes
    [col_object.append(x[0]) for x in col_types if (x[1] == 'object')]

    return col_object

# -----------------------------------------------------------------------------

def df_numeric_cols(col_types):
    col_numeric  = []

    # col[0] = colname, col[1] = dtypes
    [col_numeric.append(x[0]) for x in col_types if (x[1] == 'float64' or x[1] == 'int64')]

    return col_numeric

# -----------------------------------------------------------------------------

def load_dataframe(ext, new_tmp_path, sep):
    if (ext == 'xls' or ext == 'xlsx'):
        df = pd.read_excel(new_tmp_path, engine='openpyxl')

    else:
        df = pd.read_csv(new_tmp_path, sep=sep)

    return df