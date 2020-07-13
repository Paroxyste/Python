import pandas as pd

def clean_data(df):
    df.iloc[:,0] = pd.to_datetime(df.iloc[:,0])
    df.iloc[:,0] = df.iloc[:,0].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))

    print('- Datatime format => Done\n')

    df = df.fillna(0)
    df = df.dropna()

    print('- Data cleaned => Done\n')

    return df