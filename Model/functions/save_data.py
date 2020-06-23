import numpy as np
import os

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