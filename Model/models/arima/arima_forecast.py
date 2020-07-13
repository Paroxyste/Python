from functions.make_folder       import *
from functions.save_data         import *
from statsmodels.tsa.arima_model import ARIMA

import pandas as pd

def arima_forecast(model_fit, date_start, date_stop, path):

    forecast = model_fit.predict(start=date_start, 
                                 end=date_stop, 
                                 typ='levels')

    print('- Compute forecast => Done\n')

    forecast = pd.DataFrame(forecast)

    forecast.reset_index(level=0, inplace=True)
    forecast.columns = ['time', 'yhat']

    print('- Forecast DataFrame => Done\n')

    path_file = path + 'arima_forecast.txt'

    data = forecast

    data_name = path_file.rsplit('\\', 1)
    data_name = data_name[1]

    make_folder(path)
    save_data(data, data_name, path_file)

    return forecast