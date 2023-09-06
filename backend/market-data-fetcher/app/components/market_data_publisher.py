from app.components.errors import MarketDataFetcherError
from app.components.security import Security, get_quotes
from flask import current_app
import redis
import json

MARKET_DATA_CHANNEL = "market-data-channel"


class MarketDataPublisher:
    def __init__(self):
        """
        Initialize the default market data publisher instance.
        """
        pass

    def init_app(self, app):
        """
        Initialize the market data publisher from the flask app instance.

        :param app: The Flask app instance
        """

        self._url = app.config.get("REDIS_URL")
        self._redis = redis.from_url(self._url)
        self.ping()
        print(f"Successfully connected to redis '{self._url}' url")

    def ping(self):
        """
        Pings the redis cache instance.
        """
        if not self._redis.ping():
            raise MarketDataFetcherError(f"Cannot connect to redis '{self._url}' url")

    def publish_security_quotes(self, securities: list[Security]):
        """
        Publish security quotes.

        :param quotes: The quotes list.
        """
        self.__publish_message(MARKET_DATA_CHANNEL, json.dumps(get_quotes(securities)))

    def __publish_message(self, channel: str, message: str):
        subscribers_count = self._redis.publish(channel, message)
        current_app.logger.info(
            f"Message '{message}' has been delivered to {subscribers_count} subscribers"
        )
