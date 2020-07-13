import pandas as pd

def save_data(data, data_name, path_file):
    data.to_csv(path_file, header=True, index=None, mode='w')

    print('\n', data_name, 'has been saved ! \n +\
          Your file is in %s \n' % path_file)