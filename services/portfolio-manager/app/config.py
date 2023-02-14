import os
import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

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

# Order matters:
# SQLALchemy must be initialized before Marshmallow
# Init database
db = SQLAlchemy(app)

# Init Marshmallow
ma = Marshmallow(app)