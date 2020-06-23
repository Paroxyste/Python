import numpy as np

def matrix_2d(date, results):
    date = np.asarray(date)
    results = np.asarray(results)

    arr_len = len(date)

    date = date.reshape(arr_len, 1)
    results = results.reshape(arr_len, 1)

    new_matrix = np.concatenate((date, results), axis=1)

    print('- 2D MATRIX : [OK]\n')
    
    return new_matrix