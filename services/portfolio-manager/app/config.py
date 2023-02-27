import os
import pathlib
import connexion
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
# from flask_login import LoginManager

class Config(object):
    # The database connection URI used for the default engine
    # URI form: dialect+driver://username:password@host:port/database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite://")

    # Disables tracking of modifications to the SQLAlchemy session
    # The tracking is required by Flask-SQLAlchemy event notification
    # system that is built on top of the SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Makes sure that DB connections from the pool are still valid.
    # It's importation for entire application since many DBaaS options
    # automatically close idle connections
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True
    }

    # A secret key is used for signing cookies. The secret key is
    # required by session object which is built on top of cookies.
    # Session object is a dict that stores information specific to
    # a user from one request to the next
    SECRET_KEY = os.getenv("SECRET_KEY", "6JxOu5c4BAisvy75gRY_XFVHL1lSYQ27vvc697jV93M")

    # Bcrypt is set as a default SECURITY_PASSWORD_HASH, which requires a salt
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT", "227715728343296763842042730683926547108")

    # Restricts the "Remember Me" cookie to first-party or same-site context
    REMEMBER_COOKIE_SAMESITE = "Strict"

    # The amount of time before the cookie expires
    REMEMBER_COOKIE_DURATION = timedelta(hours=12)

    # Prevents sending cookies with all external requests which means
    # that cookies will be sent only from the origin for which it was set for
    SESSION_COOKIE_SAMESITE = "Strict"

# Flask app is created internally
basedir = pathlib.Path(__file__).parent.resolve()
connexion_app = connexion.FlaskApp(__name__, specification_dir=basedir.parent)

# Get underlying Flask app
app = connexion_app.app
app.config.from_object("config.Config")

# SQLALchemy must be initialized before Marshmallow
db = SQLAlchemy(app)

# Init Marshmallow
ma = Marshmallow(app)