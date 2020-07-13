from fbprophet             import Prophet
from functions.make_folder import *
from functions.save_data   import *

import pandas as pd

def prophet_forecast(model_fit, future, path):
    forecast = model_fit.predict(future)
    forecast[['ds', 'yhat']].tail()

    print('- Compute forecast => Done\n')

    forecast = pd.DataFrame(forecast)
    forecast = forecast[['ds', 'yhat_lower', 'yhat', 'yhat_upper']]

    print('- Forecast DataFrame => Done\n')

    path_file = path + 'prophet_forecast.txt'

    data = forecast

    data_name = path_file.rsplit('\\', 1)
    data_name = data_name[1]

    make_folder(path)
    save_data(data, data_name, path_file)

    return forecast