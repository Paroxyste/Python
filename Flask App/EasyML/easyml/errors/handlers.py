from flask import Blueprint 
from flask import render_template

# -----------------------------------------------------------------------------
# Init err

err = Blueprint('err', __name__)

# -----------------------------------------------------------------------------
# Error 404

@err.app_errorhandler(404)

def error_404(error):
    return render_template('errors/404.html',
                           title='EasyML - Lost in space ?'), 404