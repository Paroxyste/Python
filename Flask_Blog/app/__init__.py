from flask            import Flask
from flask_bcrypt     import Bcrypt
from flask_login      import LoginManager
from flask_mail       import Mail
from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)

# -----------------------------------------------------------------------------
# Database Config

app.config['SECRET_KEY'] = '448cb4ea09507a2e6bab663063e5fc58'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///config.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# -----------------------------------------------------------------------------
# Flask Mail - Default Config
# https://pythonhosted.org/Flask-Mail/
#
# app.config['MAIL_SERVER']         =   'localhost'
# app.config['MAIL_PORT']           =   25
# app.config['MAIL_USE_SSL']        =   False
# app.config['MAIL_USE_TLS']        =   False
# app.config['MAIL_USERNAME']       =   None
# app.config['MAIL_PASSWORD']       =   None
# app.config['MAIL_DEFAULT_SENDER'] =   None
# -----------------------------------------------------------------------------
# Mail Server Config

app.config['MAIL_SERVER']   = 'smtp.gmail.com'
app.config['MAIL_PORT']     = 587
app.config['MAIL_USE_SSL']  = False
app.config['MAIL_USE_TLS']  = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

mail = Mail(app)

# -----------------------------------------------------------------------------
# Login Manager

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'warning'

# -----------------------------------------------------------------------------
# Import Routes

from app import routes