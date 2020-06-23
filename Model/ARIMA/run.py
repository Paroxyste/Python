# -----------------------------------------------------------------------------
# Import modules

from ..functions.datetime_index import *
from ..functions.extract_data   import *
from ..functions.loading_data   import *
from ..functions.matrix_2d      import *
from ..functions.read_params    import *
from ..functions.save_data      import *

from ARIMA.models.arima_model import *

import configparser
import sys

# -----------------------------------------------------------------------------
# Build run function

def run(config):
    df = loading_data(CSV_DATA, 
                      separator, 
                      resampler)

    model_fit = arima_model(df, 
                            p, 
                            d, 
                            q)

    results = extract_data(model_fit, 
                           DATE_START, 
                           TIME_START, 
                           DATE_STOP, 
                           TIME_STOP)

    date = datetime_index(resampler, 
                          DATE_START, 
                          TIME_START, 
                          DATE_STOP, 
                          TIME_STOP)

    new_matrix = matrix_2d(date, 
                           results)

    save_data(MATRIX_OUTPUT, 
              new_matrix)

# -----------------------------------------------------------------------------
# Check parameters

if (len(sys.argv) != 8):
    print('\nLIST OF PARAMETERS :\n')
    print('CSV_DATA = C:\\Users\\Folder\\FolderContainCSV\\csv_file_name.csv')
    print('\nDATE_START = Start Date (YYYY-mm-dd)')
    print('TIME_START = Start Time (HH:MM:SS)')
    print('\nDATE_STOP = Stop Date  (YYYY-mm-dd)')
    print('TIME_STOP = Start Time (HH:MM:SS)')
    print('\nMATRIX_OUTPUT = C:\\Users\\Folder\\FolderForMatrixOutput\\my_matrix.txt')
    print('\nCONFIG_FILE = C:\\Users\\Folder\\Conf\\config.txt')

else :
    CSV_DATA      = sys.argv[1]
    DATE_START    = sys.argv[2]
    TIME_START    = sys.argv[3]
    DATE_STOP     = sys.argv[4]
    TIME_STOP     = sys.argv[5]
    MATRIX_OUTPUT = sys.argv[6]
    CONFIG_FILE   = sys.argv[7]

    # Get config file
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    # Get params from config file 
    separator = str(read_params(config, 'ARIMA', 'separator', ';'))
    resampler = str(read_params(config, 'ARIMA', 'resampler', '15T'))

    p = int(read_params(config, 'ARIMA', 'p', 2))
    d = int(read_params(config, 'ARIMA', 'd', 0))
    q = int(read_params(config, 'ARIMA', 'q', 2))

    run(config)