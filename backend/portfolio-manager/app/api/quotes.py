from app.components.market_data_subscriber import market_data_subscriber
from app.components.market_data_fetcher import market_data_fetcher
from app.components.errors import make_error_response
from flask_jwt_extended import get_current_user, jwt_required
from flask import (
    current_app,
    stream_with_context,
    Response,
)
import redis
import json

MARKET_DATA_CHANNEL = "market-data-channel"


def filter_quotes_by_securities(quotes: dict, securities: list[str]) -> dict:
    result = {}
    for security, price in quotes.items():
        if security in securities:
            result[security] = price
    return result


def wrap_quotes(quotes: dict) -> str:
    return f"data: {json.dumps(quotes)} \n\n"


@jwt_required()
def stream(securities):
    current_app.logger.info(f"Subscribe for {securities} quotes streaming")
    try:
        quotes = market_data_fetcher.subscribe_for_quotes(securities)
        current_app.logger.info(f"Quotes: {quotes}")
        current_user = get_current_user()
        subscriber = market_data_subscriber.subscribe(MARKET_DATA_CHANNEL)

        def generator(quotes):
            try:
                # Stream the quotes being received upon the request to the market-data-fetcher
                yield wrap_quotes(quotes)

                # Stream the quotes from regular updates
                for payload in subscriber.listen():
                    current_app.logger.info(f"Redis payload: {payload}")
                    if payload["type"] == "message":
                        quotes = json.loads(payload["data"])
                        quotes = filter_quotes_by_securities(
                            quotes=quotes, securities=securities
                        )
                        current_app.logger.info(
                            f"Send quotes: {quotes} for user {current_user.id}"
                        )
                        yield wrap_quotes(quotes)
            finally:
                try:
                    subscriber.unsubscribe(MARKET_DATA_CHANNEL)
                    current_app.logger.info(
                        f"A user {current_user.id} successfully unsibscribed from quotes streaming"
                    )
                except redis.ConnectionError:
                    current_app.logger.error(
                        f"A user {current_user.id} cannot unsubscribe"
                    )

        current_app.logger.info(
            f"A user {current_user.id} successfully subscribed for {securities} quotes streaming"
        )
        # stream_with_context will keep the request context active during the generator
        return Response(
            stream_with_context(generator(quotes)), content_type="text/event-stream"
        )
    except Exception as error:
        current_app.logger.error(f"Unable to subscribe to quotes. {error}")
        return make_error_response(500, f"Unable to subscribe to quotes. {error}")
