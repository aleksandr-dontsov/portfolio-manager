import os
from datetime import timedelta


class Config(object):
    """Base configuration"""

    # Disable debugging
    DEBUG = False

    # Disables testing mode
    TESTING = False

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
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    # A secret key is used for signing cookies. The secret key is
    # required by session object which is built on top of cookies.
    # Session object is a dict that stores information specific to
    # a user from one request to the next
    SECRET_KEY = os.getenv("SECRET_KEY", "BAD_SECRET_KEY")

    # Bcrypt is set as a default SECURITY_PASSWORD_HASH, which requires a salt
    SECURITY_PASSWORD_SALT = os.getenv(
        "SECURITY_PASSWORD_SALT", "BAD_SECURITY_PASSWORD_SALT"
    )

    # Enables the change password endpoint
    SECURITY_CHANGEABLE = True

    # Specifies the password change url
    SECURITY_CHANGE_URL = "/api/change_password"

    # Returns 401 code and static html for authentication failures rather than 302 code
    SECURITY_BACKWARDS_COMPAT_UNAUTHN = True

    # Restricts the "Remember Me" cookie to first-party or same-site context
    REMEMBER_COOKIE_SAMESITE = "Strict"

    # The amount of time before the cookie expires
    REMEMBER_COOKIE_DURATION = timedelta(hours=12)

    # Prevents sending cookies with all external requests which means
    # that cookies will be sent only from the origin for which it was set for
    SESSION_COOKIE_SAMESITE = "Strict"


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True


class TestingConfig(Config):
    """Testing configuration"""

    TESTING = True

    # Disables all CSRF protection
    WTF_CSRF_ENABLED = False

    # Specifies the plaintext as the password hash algorithm
    SECURITY_PASSWORD_HASH = "plaintext"
