from statsmodels.tsa.arima_model import ARIMA

import pandas as pd

def arima_model(df, p, d, q):
    df = df.set_index(df.columns[0])

    model = ARIMA(df, 
                  order=(p,d,q))

    model_fit = model.fit(disp=-1)

    print('\n- ARIMA is ready !\n')

    return model_fit