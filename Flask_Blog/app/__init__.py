from app.config       import Config
from flask            import Flask
from flask_bcrypt     import Bcrypt
from flask_login      import LoginManager
from flask_mail       import Mail
from flask_sqlalchemy import SQLAlchemy

# -----------------------------------------------------------------------------
# Init App

db = SQLAlchemy()
bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'warning'

mail = Mail()

# -----------------------------------------------------------------------------
# Create App

def create_app(config_class  = Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # init components
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # import routes
    from app.users.routes import users
    from app.posts.routes import posts
    from app.main.routes  import main

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app
