def extract_data(model_fit, DATE_START, TIME_START, DATE_STOP, TIME_STOP):
    start = DATE_START + ' ' + TIME_START
    stop  = DATE_STOP  + ' ' + TIME_STOP

    results = model_fit.predict(start=start, 
                                end=stop, 
                                typ='levels')

    print('- GET PREDICT VALUES : [OK]\n')

    return results