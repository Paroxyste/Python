# -----------------------------------------------------------------------------
# Import modules

import numpy  as np
import os
import pandas as pd
import pickle
import re
import sys

from datetime import datetime, timedelta
from statsmodels.tsa.arima_model import ARIMA

# -----------------------------------------------------------------------------
# CHECK PARAMETERS

if (len(sys.argv) != 9):
    print('LIST OF PARAMETERS :\n')
    print('\nCSV_DATA = C:\\Users\\Folder\\FolderContainCSV\\csv_file_name.csv')
    print('\nSEP = \\t or \s or ; or ,')
    print('\nTIME_RES = XXT (XX is an integer || T = minutes)')
    print('\nDATE_START = Start Date (YYYY-mm-dd)')
    print('TIME_START = Start Time (HH:MM:SS)')
    print('\nDATE_STOP = Stop Date  (YYYY-mm-dd)')
    print('TIME_STOP = Start Time (HH:MM:SS)')
    print('\nMATRIX_OUTPUT = C:\\Users\\Folder\\FolderForMatrixOutput\\my_matrix.txt')

else :
    # CSV path <str>
    CSV_DATA = sys.argv[1]

    # Separator <str>
    SEP = sys.argv[2]

    # Resample <str>
    TIME_RES = sys.argv[3]

    # Start Date : YYYY-MM-DD <str>
    DATE_START = sys.argv[4]

    # Start Time : HH:MM:SS <str>
    TIME_START = sys.argv[5]
    
    # Stop Date : YYYY-MM-DD <str>
    DATE_STOP = sys.argv[6]

    # Stop Time : HH:MM:SS <str>
    TIME_STOP = sys.argv[7]

    # Matrix path <str>
    MATRIX_OUTPUT = sys.argv[8]

# -----------------------------------------------------------------------------
# LOADING_DATA

def loading_data(CSV_DATA, SEP, TIME_RES):
    df = pd.read_csv(CSV_DATA, 
                     sep=';', 
                     parse_dates=[0], 
                     index_col=0)

    df = df.resample(TIME_RES).first().reindex(columns=df.columns)

    print('- DATA LOADED : [OK]\n')

    return df

# -----------------------------------------------------------------------------
# CLEAN_DATA

def clean_data(df):
    df = df.fillna(0)
    df.dropna()
    
    print('- DATA CLEANED : [OK]\n')

    return df

# -----------------------------------------------------------------------------
# ARIMA_MODEL

def arima_model(df):
    model = ARIMA(df, 
                  order=(2,0,2))

    model_fit = model.fit(disp=-1)

    print('- MODEL READY : [OK]\n')

    return model_fit

# -----------------------------------------------------------------------------
# START_DATE

def start_date(DATE_START, TIME_START):
    start = DATE_START + ' ' + TIME_START

    return start

# -----------------------------------------------------------------------------
# STOP_DATE

def stop_date(DATE_STOP, TIME_STOP):
    stop = DATE_STOP + ' ' + TIME_STOP

    return stop

# -----------------------------------------------------------------------------
# EXTRACT_DATA

def extract_data(model_fit, start, stop):
    results = model_fit.predict(start=start, 
                                end=stop, 
                                typ='levels')

    print('- GET PREDICT VALUES : [OK]\n')

    return results

# -----------------------------------------------------------------------------
# DATETIME_INDEX

def datetime_index(TIME_RES, start, stop):
    interval = re.sub('[^0-9]', '', TIME_RES)
    interval = int(interval)

    ind_start = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
    ind_end   = datetime.strptime(stop, '%Y-%m-%d %H:%M:%S')

    seconds = (ind_end - ind_start).total_seconds()

    step = timedelta(minutes=interval)

    date = []

    for i in range(0, int(seconds), int(step.total_seconds())) :
        date_value = ind_start + timedelta(seconds=i)
        date.append(date_value.strftime('%Y-%m-%dT%H:%M:%S'))

    stop = stop.replace(' ' , 'T') 
    date.append(stop)

    print('- GET DATETIME INDEX : [OK]\n')
    
    return date

# -----------------------------------------------------------------------------
# MATRIX_2D

def matrix_2d(date, results):
    date = np.asarray(date)
    results = np.asarray(results)

    arr_len = len(date)

    date = date.reshape(arr_len, 1)
    results = results.reshape(arr_len, 1)

    new_matrix = np.concatenate((date, results), axis=1)

    print('- 2D MATRIX : [OK]\n')
    
    return new_matrix

# -----------------------------------------------------------------------------
# SAVE_DATA

def save_data(MATRIX_OUTPUT, new_matrix):
    output_matrix = MATRIX_OUTPUT.rsplit('\\', 1)
    output_matrix_dir = output_matrix[0]

    try :
        os.mkdir(output_matrix_dir)

    except OSError:
        print('- Folder already existing\n')

    else :
        print('- Folder successfully created !\n')

    np.savetxt(MATRIX_OUTPUT, new_matrix, fmt='%s')

    print('\nThe file has been saved ! \n +\
        Your file is in %s \n' % MATRIX_OUTPUT)

# -----------------------------------------------------------------------------
# MAIN

def main():
    df = clean_data(loading_data(CSV_DATA, SEP, TIME_RES))

    model_fit = arima_model(df)

    start = start_date(DATE_START, TIME_START)
    stop = stop_date(DATE_STOP, TIME_STOP)

    results = extract_data(model_fit, start, stop)

    date = datetime_index(TIME_RES, start, stop)

    new_matrix = matrix_2d(date, results)

    save_data(MATRIX_OUTPUT, new_matrix)

main()