from fbprophet import Prophet

def prophet_future(model_fit, days, freq):
    future = model_fit.make_future_dataframe(periods=days, 
                                             freq=freq)

    print('- Forecast datetime => Done\n')

    return future