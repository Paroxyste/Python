from fbprophet.diagnostics import cross_validation

def prophet_cv(model_fit, initial, period, horizon) :
    df_cv = cross_validation(model_fit, 
                             initial=initial, 
                             period=period, 
                             horizon=horizon)

    print('\n- Cross validation => Done\n')

    return df_cv