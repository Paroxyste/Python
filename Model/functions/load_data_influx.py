from functions.clean_data import *
from influxdb             import InfluxDBClient

import pandas as pd

def load_data_influx(server_name, server_port, user_name, user_pass, db_name, request):
    client = InfluxDBClient(server_name, 
                            server_port, 
                            user_name, 
                            user_pass, 
                            db_name)

    req = client.query(request);

    res = list(req.get_points(measurement='value'))

    df = pd.DataFrame(res)

    print('\n- Data loaded => Done\n')

    df = clean_data(df)

    return df