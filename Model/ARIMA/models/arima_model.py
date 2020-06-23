from statsmodels.tsa.arima_model import ARIMA

def arima_model(df, p, d, q):
    model = ARIMA(df, 
                  order=(p,d,q))

    model_fit = model.fit(disp=-1)

    print('- MODEL READY : [OK]\n')

    return model_fit