class Config(object):
    """Base configuration"""

    # Disable debugging
    DEBUG = False

    # Disables testing mode
    TESTING = False

    # Alpha Vantage API key
    ALPHA_VANTAGE_API_KEY = "VI7YS8B4N0TLBIYJ"


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True
