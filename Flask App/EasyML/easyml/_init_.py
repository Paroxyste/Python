# -----------------------------------------------------------------------------

from flask         import Flask
from flask_mysqldb import MySQL

# -----------------------------------------------------------------------------
# Prepare mysql database
mysql = MySQL()

# -----------------------------------------------------------------------------
# App config
def create_app():
    app = Flask(__name__)
    app.config.from_object('config.LocalConfig')

    app.secret_key = app.config['SECRET_KEY']

    # -------------------------------------------------------------------------
    # Init component
    mysql.init_app(app)

    # -------------------------------------------------------------------------
    # Import routes

    from easyml.exploratory.routes import exp
    from easyml.clustering.routes  import clust
    from easyml.errors.handlers    import err
    from easyml.main.routes        import main
    from easyml.regression.routes  import reg
    from easyml.rein_learn.routes  import rf
    from easyml.users.routes       import users

    app.register_blueprint(exp)
    app.register_blueprint(clust)
    app.register_blueprint(err)
    app.register_blueprint(main)
    app.register_blueprint(reg)
    app.register_blueprint(rf)
    app.register_blueprint(users)

    return app