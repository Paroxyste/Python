# -----------------------------------------------------------------------------
# Server Config

class Config :
    # app server
    SECRET_KEY = '448cb4ea09507a2e6bab663063e5fc58'
    SQLALECHEMY_DATABASE_URI = 'sqlite:///config.db'

    # mail server
    MAIL_SERVER   = 'smtp.gmail.com'
    MAIL_PORT     = 587
    MAIL_USE_SSL  = False
    MAIL_USE_TLS  = True
    MAIL_USERNAME = 'contact@admin.fr'
    MAIL_PASSWORD = 'password'