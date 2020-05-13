from flask import redirect, render_template, request, session, url_for
from shop  import app, db

@app.route('/')
def home():
    return 'Home Page'

@app.route('/register')
def register():
    return render_template('admin/register.html', title = 'Register')