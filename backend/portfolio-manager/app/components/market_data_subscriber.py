from app.components.errors import PortfolioManagerError
import redis


# Market Data Subscriber
class MarketDataSubscriber:
    def __init__(self):
        pass

    def init_app(self, app):
        url = app.config.get("REDIS_URL")
        self._redis = redis.from_url(url, decode_responses=True)
        if not self._redis.ping():
            app.logger.error(f"Cannot connect to redis '{url}' url")
            raise PortfolioManagerError(f"Cannot connect to redis '{url}' url")
        app.logger.info(f"Successfully connected to redis '{url}' url")

    def subscribe(self, channel: str):
        pubsub = self._redis.pubsub(ignore_subscribe_messages=True)
        pubsub.subscribe(channel)
        return pubsub


# Init Market Data Subscriber
market_data_subscriber = MarketDataSubscriber()
