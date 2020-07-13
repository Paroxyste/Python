import os

def make_folder(path):
    try :
        os.mkdir(path)

    except OSError:
        print('- Folder already existing\n')

    else :
        print('- Folder successfully created !\n')
