from datetime import datetime, timedelta

import re

def datetime_index(resampler, DATE_START, TIME_START, DATE_STOP, TIME_STOP):
    start = DATE_START + ' ' + TIME_START
    stop  = DATE_STOP  + ' ' + TIME_STOP

    interval = re.sub('[^0-9]', '', resampler)
    interval = int(interval)

    ind_start = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
    ind_end   = datetime.strptime(stop,  '%Y-%m-%d %H:%M:%S')

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