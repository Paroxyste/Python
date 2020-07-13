from fbprophet.diagnostics import performance_metrics
from functions.make_folder import *
from functions.save_data   import *

def prophet_pm(df_cv, path) :
    df_pm = performance_metrics(df_cv)

    print('- Mean absolute error => Done\n')

    df_pm = df_pm[['horizon', 'mae']]

    path_file = path + 'prophet_accuracy.txt'

    data = df_pm

    data_name = path_file.rsplit('\\', 1)
    data_name = data_name[1]

    make_folder(path)
    save_data(data, data_name, path_file)

    return df_pm
