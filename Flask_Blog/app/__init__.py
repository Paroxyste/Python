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

def create_app():
    app = Flask(__name__)

    # config server
    app.config['SECRET_KEY'] = '448cb4ea09507a2e6bab663063e5fc58'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///config.db'

    # init server
    bcrypt.init_app(app)
    db.init_app(app)

    # config mail server
    # Enable this option after logging to Gmail to make it work.
    # -> https://www.google.com/settings/security/lesssecureapps
    app.config['MAIL_SERVER']   = 'smtp.gmail.com'
    app.config['MAIL_PORT']     = 587
    app.config['MAIL_USE_SSL']  = False
    app.config['MAIL_USE_TLS']  = True
    app.config['MAIL_USERNAME'] = 'contact@gmail.com'
    app.config['MAIL_PASSWORD'] = 'gmail_password'

    # init mail server
    mail.init_app(app)

    # init login manager
    login_manager.init_app(app)

    # import routes
    from app.errors.handlers import errors
    from app.main.routes     import main
    from app.posts.routes    import posts
    from app.users.routes    import users

    app.register_blueprint(errors)
    app.register_blueprint(main)
    app.register_blueprint(posts)
    app.register_blueprint(users)

    return app