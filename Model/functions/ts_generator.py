from datetime import datetime, timedelta
import numpy as np

def ts_generator(date_start, date_stop) :
    start  = datetime.strptime(date_start, '%Y-%m-%d %H:%M:%S')
    finish = datetime.strptime(date_stop , '%Y-%m-%d %H:%M:%S')

    seconds = (finish - start).total_seconds()
    step    = timedelta(minutes=15)

    array = []

    for i in range(0, int(seconds), int(step.total_seconds())):
        date_value = start + timedelta(seconds=i)
        array.append(date_value.strftime('%Y-%m-%d %H:%M:%S'))

    dates = np.asarray(array)

    x = len(dates)

    datas = np.random.randint(4, size=x)
    datas = np.asarray(datas)

    dates = dates.reshape(x, 1)
    datas = datas.reshape(x, 1)

    metrics = np.concatenate((dates, datas), axis=1)

    np.savetxt('TS_generator.txt', metrics, fmt='%s', delimiter=',')

ts_generator('2020-01-01 00:00:00', '2022-02-02 12:30:00')