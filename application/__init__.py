from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import mkdir

from .configs import DATABASE_PATH, SOLUTIONS_DIR


# Initializes app and configures it
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(DATABASE_PATH) + '/aoc_share.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creates the db's directories if they don't exists
if not DATABASE_PATH.exists():
    mkdir(DATABASE_PATH)
if not SOLUTIONS_DIR.exists():
    mkdir(SOLUTIONS_DIR)

# Initializes db
db = SQLAlchemy(app)

# Creates all the models
from .models import *
db.create_all()

# Populates the db if it's empty
if not Update.query.first():
    from .scraper import populate_db
    populate_db()

# Routes the routes
from .routes import *
