from fbprophet import Prophet

import datetime
import pandas as pd

def prophet_model(df):
    df = df.rename(columns={df.columns[0]: 'ds', 
                            df.columns[1]: 'y'})

    model = Prophet()
    model_fit = model.fit(df)

    print('\n- Prophet is ready !\n')

    return model_fit
