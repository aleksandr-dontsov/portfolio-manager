import os
import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager

class Config(object):
    # The database connection URI used for the default engine
    # URI form: dialect+driver://username:password@host:port/database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite://")

    # Disables tracking of modifications to the SQLAlchemy session
    # The tracking is required by Flask-SQLAlchemy event notification
    # system that is built on top of the SQLAlchemy.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask app is created internally
basedir = pathlib.Path(__file__).parent.resolve()
connexion_app = connexion.FlaskApp(__name__, specification_dir=basedir.parent)

# Get underlying Flask app
app = connexion_app.app
app.config.from_object("config.Config")
# A secret key is used for signing cookies. The secret key is
# required by session object which is built on top of cookies.
# Session object is a dict that stores information specific to
# a user from one request to the next
app.secret_key = 'cb9cfe2d0461f8dbaefbb7d73514f71cd733319376ab24dd5e5c487fc57e7efb'

# SQLALchemy must be initialized before Marshmallow
db = SQLAlchemy(app)

# Init Marshmallow
ma = Marshmallow(app)

# Init LoginManager that allows the app and Flask-Login work together
login_manager = LoginManager(app)