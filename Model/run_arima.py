# -----------------------------------------------------------------------------
# Import functions

from functions.load_data_influx import *
from functions.read_params      import *

from models.arima.arima_model    import *
from models.arima.arima_forecast import *

import configparser
import sys

# -----------------------------------------------------------------------------
# Build run function

def run_arima(config):
    df = load_data_influx(server_name,
                          server_port,
                          user_name,
                          user_pass,
                          db_name, 
                          request)

    model_fit = arima_model(df, p, d, q)

    forecast = arima_forecast(model_fit,
                              date_start,
                              date_stop,
                              path)

# -----------------------------------------------------------------------------
# Check parameters

if (len(sys.argv) != 2):
    print('\nLIST OF PARAMETERS :\n')
    print('\nCONFIG_FILE = C:\\Users\\Folder\\Conf\\config.txt')

else :
    # python3     = sys.argv[0]
    CONFIG_FILE   = sys.argv[1]

    # Get config file
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    # Get params from config file 
    server_name = str(read_params(config , 'INFLUX' , 'server_name' , ''))
    server_port = str(read_params(config , 'INFLUX' , 'server_port' , ''))
    user_name   = str(read_params(config , 'INFLUX' , 'user_name'   , ''))
    user_pass   = str(read_params(config , 'INFLUX' , 'user_pass'   , ''))
    db_name     = str(read_params(config , 'INFLUX' , 'db_name'     , ''))

    request = str(read_params(config , 'REQUEST' , 'request' , ''))

    p = int(read_params(config , 'ARIMA' , 'p' , ''))
    d = int(read_params(config , 'ARIMA' , 'd' , ''))
    q = int(read_params(config , 'ARIMA' , 'q' , ''))

    date_start = str(read_params(config , 'DATA' , 'date_start' , ''))
    date_stop  = str(read_params(config , 'DATA' , 'date_stop'  , ''))

    path = str(read_params(config , 'OUTPUT' , 'path' , '.'))

    run_arima(config)
