import pandas as pd

def loading_data(CSV_DATA, separator, resampler):
    df = pd.read_csv(CSV_DATA, 
                     sep=separator, 
                     parse_dates=[0], 
                     index_col=0)

    df = df.resample(resampler).first().reindex(columns=df.columns)

    print('- DATA LOADED : [OK]\n')

    df = df.fillna(0)
    df.dropna()
    
    print('- DATA CLEANED : [OK]\n')

    return df