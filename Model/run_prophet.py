# -----------------------------------------------------------------------------
# Import functions

from functions.load_data_influx import *
from functions.read_params      import *

from models.prophet.prophet_model    import *
from models.prophet.prophet_future   import *
from models.prophet.prophet_forecast import *
from models.prophet.prophet_cv       import *
from models.prophet.prophet_pm       import *

import configparser
import sys

# -----------------------------------------------------------------------------
# Build run function

def run(config):
    df = load_data_influx(server_name,
                          server_port,
                          user_name,
                          user_pass,
                          db_name, 
                          request)

    model_fit = prophet_model(df)

    future = prophet_future(model_fit,
                            days,
                            freq)

    forecast = prophet_forecast(model_fit,
                                future,
                                path)

    df_cv = prophet_cv(model_fit,
                       initial,
                       period,
                       horizon)

    df_pm = prophet_pm(df_cv, 
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

    days    = int(read_params(config , 'PROPHET' , 'days'    , 7))
    freq    = str(read_params(config , 'PROPHET' , 'freq'    , 'T'))
    initial = str(read_params(config , 'PROPHET' , 'initial' , '42 days'))
    period  = str(read_params(config , 'PROPHET' , 'period'  , '7 days'))
    horizon = str(read_params(config , 'PROPHET' , 'horizon' , '21 days'))

    path = str(read_params(config , 'OUTPUT' , 'path' , '.'))

    run(config)
