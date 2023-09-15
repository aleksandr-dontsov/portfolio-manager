import os
from datetime import timedelta


class Config(object):
    """Base configuration"""

    # Disable debugging
    DEBUG = False

    # Disables testing mode
    TESTING = False

    user = os.environ["POSTGRES_USER"]
    password = os.environ["POSTGRES_PASSWORD"]
    hostname = os.environ["POSTGRES_HOSTNAME"]
    port = os.environ["POSTGRES_PORT"]
    database = os.environ["APPLICATION_DB"]

    # The database connection URI used for the default engine
    # URI form: dialect+driver://username:password@host:port/database
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{user}:{password}@{hostname}:{port}/{database}"
    )

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

    # The secret key is used to decode/encode JWTs when using a symmetric signing algorithm
    # If this value is not`` set, SECRET_KEY value will be used instead
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "BAD_JWT_SECRET_KEY")

    # Specifies for how long an access token should be valid before it expires
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)

    # Specifies where to look for a JWT when processing a request
    # Benefits of using cookies over headers:
    # 1. Can be configured to send only over HTTPS
    # 2. Prevents XSS attacks from being able to steal the JTW,
    #    because they are stored in http-only cookie
    # 3. Implicit refresh of JWTs that are close to expiring
    JWT_TOKEN_LOCATION = ["cookies"]

    # Controls if the secure web flag should be placed on cookies created by this extenstion.
    # If a cookie is markeds as secure it will only be sent via HTTPS
    JWT_COOKIE_SECURE = False

    # Controls if the cookies are configured as session cookies,
    # which are deleted once a browser is closed
    JWT_SESSION_COOKIE = True

    # Controls if the CSRF double submit token will be stored in additional cookies.
    JWT_CSRF_IN_COOKIES = True

    # A minimum password length
    MIN_PASSWORD_LENGTH = 8

    # Alpha Vantage API key
    ALPHA_VANTAGE_API_KEY = "VI7YS8B4N0TLBIYJ"

    # Redis URL
    REDIS_URL = os.getenv("REDIS_URL")

    # Allow requests from the frontend
    CORS_ORIGINS = "http://localhost:3000"

    # Market Data Fetcher URL
    MARKET_DATA_FETCHER_BASE_URL = "http://market-data-fetcher:5000/api/v1"

    # Securities update interval
    SECURITIES_UPDATE_INTERVAL_HOURS = 24

    # Max number of searched securities per request
    SECURITIES_MAX_SEARCH_RESULTS = 50

    # Currency exchange rate update interval
    CURRENCY_EXCHANGE_RATE_UPDATE_INTERVAL_HOURS = 24


class ProductionConfig(Config):
    """Production configuration"""

    JWT_COOKIE_SECURE = True


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
