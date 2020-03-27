import os

# -----------------------------------------------------------------------------
# Server Config

class Config :
    # app server
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALECHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

    # mail server
    MAIL_SERVER   = 'smtp.gmail.com'
    MAIL_PORT     = 587
    MAIL_USE_SSL  = False
    MAIL_USE_TLS  = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')