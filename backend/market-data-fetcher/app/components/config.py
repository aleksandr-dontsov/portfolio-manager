import os


class Config(object):
    """Base configuration"""

    # Disable debugging
    DEBUG = False

    # Disables testing mode
    TESTING = False

    # Financial Modeling Prep API key
    FINANCIAL_MODELING_PREP_API_KEY = "e295946c2ee6656950722b49d2b11baf"

    # Financial Modeling Prep API URL
    FINANCIAL_MODELING_PREP_API_BASE_URL = "https://financialmodelingprep.com/api/v3"

    # Redis URL
    REDIS_URL = os.getenv("REDIS_URL")

    # Quotes publishing interval in seconds
    QUOTE_PUBLISHING_INTERVAL_SEC = 120

    # Currency exchange rate update interval in seconds
    CURRENCY_EXCHANGE_RATE_UPDATE_INTERVAL_SEC = 24 * 60 * 60


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True
