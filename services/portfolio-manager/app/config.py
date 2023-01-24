import os

class Config(object):
    # The database connection URI used for the default engine
    # URI form: dialect+driver://username:password@host:port/database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite://")

    # Disables tracking of modifications to the SQLAlchemy session
    # The tracking is required by Flask-SQLAlchemy event notification
    # system that is built on top of the SQLAlchemy.
    SQLALCHEMY_TRACK_MODIFICATIONS = False