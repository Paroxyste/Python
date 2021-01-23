# -----------------------------------------------------------------------------

from werkzeug.utils import secure_filename

import hashlib
import os
import random
import string

# -----------------------------------------------------------------------------

def allowed_extension(extension, lang):
    msg_err   = None
    allow_ext = ['csv', 'tsv', 'xls', 'xlsm', 'xlsx']

    if (extension not in allow_ext):

        if (lang == 'en'):
            msg_err = (
                'This extension is not supported. Please use the '
                'following formats : .csv, .tsv, .xls, .xlsx'
            )

        else:
            msg_err (
                'Cette extension n\'est pas supportée. Veuillez utiliser '
                'les formats suivants : .csv, .tsv, .xls, .xlsx.'
            )

    return msg_err

# -----------------------------------------------------------------------------

def file_check_size(size, new_tmp_path, lang):
    msg_err = None

    if (size > 100000):

        if (lang == 'en'):
            msg_err = (
                'Your file is too large. Please check that it does not '
                'exceed 100Ko.'
            )

        else:
             msg_err = (
                'Votre fichier est trop volumineux. Veuillez vérifier '
                'qu\'il ne dépasse pas 100Ko.'
            )

        file_remove(new_tmp_path)

    return msg_err

# -----------------------------------------------------------------------------

def file_extension(filename):
    ext = filename.split('.', 1)[1]
    ext = ext.lower()

    return ext

# -----------------------------------------------------------------------------

def file_get_size(new_tmp_path):
    size = os.stat(new_tmp_path).st_size

    return size

# -----------------------------------------------------------------------------

def file_remove(new_tmp_path):
    os.remove(new_tmp_path)

# -----------------------------------------------------------------------------

def file_tmp_path():
    path = 'C:\\Users\\Administrateur\\Documents\\temp\\'

    return path

# -----------------------------------------------------------------------------

def filename_encoder(path, filename, ext):
    random_str = string.ascii_lowercase + string.digits
    random_str = ''.join(random.sample(random_str, 16))

    encode_name = hashlib.md5(filename.encode())
    encode_name = encode_name.hexdigest() + random_str + '.' + ext

    old_path     = path + filename
    new_tmp_path = path + encode_name

    os.rename(old_path, new_tmp_path)

    return new_tmp_path

# -----------------------------------------------------------------------------

def filename_get(file):
    filename = secure_filename(file.filename)

    return filename