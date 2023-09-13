from apscheduler.schedulers.background import BackgroundScheduler
from app.components.market_data_api import MarketDataApi
from app.components.market_data_publisher import MarketDataPublisher
from app.components.cache import ThreadSafeCache
from app.components.security_cache import SecurityCache
from datetime import datetime, time


class Application:
    """
    The main application class.
    """

    def __init__(self):
        """
        Initialize the default application instance.
        """
        self._scheduler = BackgroundScheduler()
        self._market_data_api = MarketDataApi()
        self._market_data_publisher = MarketDataPublisher()
        self._securities = SecurityCache()
        self._symbols = ThreadSafeCache()
        self._exchange_rates = ThreadSafeCache()
        self._requires_update_after_market_close = True

    def init_app(self, app):
        """
        Initialize the application instance from the Flask app.
        """
        self._app = app
        self._market_data_api.init_app(app)
        self._market_data_publisher.init_app(app)
        self.__update_securities()
        self.__update_exchange_rates()

        # Publish quotes
        self._scheduler.add_job(
            func=self.__publish_quotes,
            id="publish-quotes",
            trigger="interval",
            seconds=app.config.get("QUOTE_PUBLISHING_INTERVAL_SEC"),
        )

        # Update exchange rates
        self._scheduler.add_job(
            func=self.__update_exchange_rates,
            id="update-exchange-rates",
            trigger="interval",
            seconds=app.config.get("CURRENCY_EXCHANGE_RATE_UPDATE_INTERVAL_SEC"),
        )
        self._scheduler.start()

    def __del__(self):
        """
        Destructs the application instance.
        """
        try:
            if self._scheduler.running():
                self._scheduler.shutdown()
        except Exception as error:
            self._app.logger.error(f"Unable to shut down the scheduler. {error}")

    def get_scheduler(self):
        """
        Gets the scheduler.
        """
        return self._scheduler

    def get_api(self):
        """
        Gets the market data api.
        """
        return self._market_data_api

    def get_publisher(self):
        """
        Gets the market data publisher.
        """
        return self._market_data_publisher

    def get_securities(self):
        """
        Gets the securities.
        """
        return self._securities

    def get_symbols(self):
        """
        Gets the cache of the symbols for quotes.
        """
        return self._symbols

    def get_exchange_rates(self):
        """
        Gets the cache of the currency exchange rates.
        """
        return self._exchange_rates

    def __update_securities(self):
        # Currently support only US stock exchanges
        SUPPORTED_EXCHANGES = ("NYSE", "NASDAQ", "BATS", "CBOE", "AMEX")
        updated_security_count = 0
        try:
            for security in self._market_data_api.get_tradable_securities_list():
                if not all(value is not None for value in security.to_dict().values()):
                    continue
                if security.get_exchange() not in SUPPORTED_EXCHANGES:
                    continue
                self._securities.update_security(security.get_symbol(), security)
                updated_security_count += 1
            self._app.logger.info(
                f"Stats: updated {updated_security_count} securities."
            )
        except Exception as error:
            self._app.logger.error(f"Unable to update the security cache. {error}.")

    def __publish_quotes(self):
        try:
            # Check if there are any requested quotes
            symbols = self._symbols.get_all_items()
            if not symbols:
                self._app.logger.info("No requested quotes to publish")
                return

            # Check market hours
            utc_now = datetime.utcnow().time()
            # NYSE and NASDAQ market hours
            market_open_utc = time(14, 30)
            market_close_utc = time(21, 0)
            if not (market_open_utc <= utc_now <= market_close_utc):
                # Update securities after the market has been closed
                if self._requires_update_after_market_close:
                    self._app.logger.info(
                        "Update securities after the market has been closed."
                    )
                    self.__update_securities()
                    self._requires_update_after_market_close = False
                self._app.logger.info("Market is closed. Nothing to publish.")
                return

            self._requires_update_after_market_close = True
            self.__update_securities()
            securities = self._securities.get_securities(symbols)
            with self._app.app_context():
                self._market_data_publisher.publish_security_quotes(securities)
        except Exception as error:
            self._app.logger.error(f"Unable to publish quotes. {error}.")

    def __update_exchange_rates(self):
        self._app.logger.info("Update exchange rates")
        try:
            self._exchange_rates.clear()
            self._exchange_rates.add_items(
                self._market_data_api.get_currency_exchange_rates()
            )
        except Exception as error:
            self._app.logger.error(
                f"Unable to update currency exchange rates. {error}."
            )


application = Application()
