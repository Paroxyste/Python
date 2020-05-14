from flask import Flask

from flask_bcrypt     import Bcrypt
from flask_login      import LoginManager
from flask_migrate    import Migrate
from flask_msearch    import Search
from flask_sqlalchemy import SQLAlchemy
from flask_uploads    import (configure_uploads, IMAGES, patch_request_class, 
                              UploadSet)

import os

basedir = os.path.abspath(os.path.dirname(__file__))

# -----------------------------------------------------------------------------
# App config

app = Flask(__name__)

# Generate with os.urandom(24).hex()
app.config['SECRET_KEY'] = ''

app.config['SQLALCHEMY_DATABASE_URI']        = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')

# -----------------------------------------------------------------------------
# Upload pics

photos = UploadSet('photos', IMAGES)

configure_uploads(app, photos)
patch_request_class(app)

# -----------------------------------------------------------------------------
# Init app

bcrypt = Bcrypt(app)
db     = SQLAlchemy(app)
search = Search()

search.init_app(app)

migrate = Migrate(app, db)

with app.app_context() :
    if (db.engine.url.drivername == 'sqlite'):
        migrate.init_app(app, db, render_as_batch = True)
    else:
        migrate.init_app(app, db)

# ------------------------------------------------------------------------------
# Login manager

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'customerLogin'
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_message = 'Pleaser login first'

# ------------------------------------------------------------------------------
# Routes

from shop.admin     import routes
from shop.customers import routes
from shop.products  import routes
from shop.carts     import carts
