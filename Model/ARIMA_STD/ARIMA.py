import numpy  as np
import os
import pandas as pd
import pickle
import re
import sys

from datetime import datetime, timedelta
from statsmodels.tsa.arima_model import ARIMA

# -----------------------------------------------------------------------------
# Script Parameters

if (len(sys.argv) != 11):
    print('LIST OF PARAMETERS :\n')
    print('\nCSV_PATH = C:\\Users\\Folder\\FolderContainCSV\\')
    print('CSV_NAME = CSVFileName (without .csv)')
    print('\nSEP = \\t or \s or ; or ,')
    print('\nTIME_RES = XXT (XX is an integer || T = minutes)')
    print('\nDATE_START = Start Date (YYYY-mm-dd)')
    print('TIME_START = Start Time (HH:MM:SS)')
    print('\nDATE_STOP = Stop Date  (YYYY-mm-dd)')
    print('TIME_STOP = Start Time (HH:MM:SS)')
    print('\nMATRIX_DIR = C:\\Users\\Folder\\FolderForMatrixOutput\\')
    print('MATRIX_NAME = nameofmymatrix (without .txt)')

else :
    # CSV path <str>
    CSV_PATH = sys.argv[1]

    # CSV Name <str>
    CSV_NAME = sys.argv[2]

    # Separator <str>
    SEP = sys.argv[3]

    # Resample <str>
    TIME_RES = sys.argv[4]

    # Start Date : YYYY-MM-DD <str>
    DATE_START = sys.argv[5]

    # Start Time : HH:MM:SS <str>
    TIME_START = sys.argv[6]
    
    # Stop Date : YYYY-MM-DD <str>
    DATE_STOP = sys.argv[7]

    # Stop Time : HH:MM:SS <str>
    TIME_STOP = sys.argv[8]

    # Matrix output directory <str>
    MATRIX_DIR = sys.argv[9]

    # Matrix output name <str>
    MATRIX_NAME = sys.argv[10]

    # -------------------------------------------------------------------------
    # Loading & Resampling Data

    print('\n----------------------- SCRIPT RUNNING -----------------------\n')

    csv = CSV_PATH + CSV_NAME + '.csv'

    df = pd.read_csv(csv, 
                    sep=';', 
                    parse_dates=[0], 
                    index_col=0)

    df = df.resample(TIME_RES).first().reindex(columns=df.columns)

    print('\n- DATA LOADED : [OK]\n')

    # -------------------------------------------------------------------------
    # Clean Data

    df = df.fillna(0)
    df.dropna()

    print('- DATA CLEANED : [OK]\n')

    # -------------------------------------------------------------------------
    # Model with default parameters

    print('- START MODEL : [OK]\n')

    model = ARIMA(df, 
                order=(2, 0, 2))

    results = model.fit(disp=-1)

    print('\n------------------------ MODEL READY ------------------------\n')

    # -------------------------------------------------------------------------
    # Extract matrix data

    start = DATE_START + ' ' + TIME_START
    end   = DATE_STOP  + ' ' + TIME_STOP

    ex_results = results.predict(start=start, 
                                 end=end, 
                                 typ='levels')

    print('\n- GET PREDICT VALUES : [OK]\n')

    # -------------------------------------------------------------------------
    # Clear interval

    interval = re.sub('[^0-9]', '', TIME_RES)
    interval = int(interval)

    # -------------------------------------------------------------------------
    # Create new index

    ind_start = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
    ind_end   = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')

    seconds = (ind_end - ind_start).total_seconds()

    step = timedelta(minutes=interval)

    date = []

    for i in range(0, int(seconds), int(step.total_seconds())) :
        date_value = ind_start + timedelta(seconds=i)
        date.append(date_value.strftime('%Y-%m-%dT%H:%M:%S'))

    end = end.replace(' ' , 'T') 
    date.append(end)

    print('- GET DATETIME INDEX : [OK]\n')

    # -------------------------------------------------------------------------
    # Create 2D matrix

    date = np.asarray(date)
    ex_results = np.asarray(ex_results)

    arr_len = len(date)

    date = date.reshape(arr_len, 1)
    ex_results = ex_results.reshape(arr_len, 1)

    new_matrix = np.concatenate((date, ex_results), axis=1)

    print('- 2D MATRIX : [OK]\n')

    # -------------------------------------------------------------------------
    # Matrix datas directory

    output_dir = MATRIX_DIR

    try :
        os.mkdir(MATRIX_DIR)

    except OSError:
        print('Failure to create the folder => Already Existing\n')

    else :
        print('Successfully created the directory !\n')

    # -------------------------------------------------------------------------
    # Matrix name output

    out_file_name = MATRIX_DIR + MATRIX_NAME + '.txt'

    np.savetxt(out_file_name, new_matrix, fmt='%s')

    print('\nThe file has been saved ! \n +\
        Your file is in %s \n' % out_file_name)

    print('\n------------------- PREDICTION SUCCESSFULLY -------------------')