from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Initializes app and configures it
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initializes db
db = SQLAlchemy(app)


# Creates all the models
from .models import *
db.create_all()
