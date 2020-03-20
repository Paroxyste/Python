from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = '448cb4ea09507a2e6bab663063e5fc58'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///config.db'

db = SQLAlchemy(app)

from app import routes