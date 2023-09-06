from app.components.errors import MarketDataFetcherError
from app.components.security import Security
from app.components.exchange_rate import ExchangeRate
import requests


# The API wrapper class over Financial Modeling Prep API
class MarketDataApi:
    def __init__(self):
        """
        Initialize the default market data api instance.
        """
        pass

    def init_app(self, app):
        """
        Initialize the market data api from the flask app instance.

        :param app: The Flask app instance
        """
        self._financial_modeling_prep_base_url = app.config.get(
            "FINANCIAL_MODELING_PREP_API_BASE_URL"
        )
        self._financial_modeling_prep_api_key = app.config.get(
            "FINANCIAL_MODELING_PREP_API_KEY"
        )

    def get_tradable_securities_list(self) -> list[Security]:
        """
        Gets all tradable securities.

        :return: The list of tradable symbols.
        """
        rows = self.__send_request("/available-traded/list")
        return [
            Security(
                row["symbol"],
                row["name"],
                row["price"],
                row["exchangeShortName"],
                row["type"],
            )
            for row in rows
        ]

    def get_currency_exchange_rates(self) -> list[ExchangeRate]:
        """
        Gets the currency exchange rates.

        :return: The currency exchange rates.
        """
        rows = self.__send_request("/fx")
        exchange_rates = []
        for row in rows:
            try:
                currencies = row["ticker"].split("/")
                exchange_rates.append(
                    ExchangeRate(currencies[0], currencies[-1], row["ask"], row["bid"])
                )
            except Exception:
                pass
        return exchange_rates

    def __send_request(self, endpoint: str) -> list:
        url = self.__make_full_url(endpoint)
        params = {"apikey": self._financial_modeling_prep_api_key}
        response = requests.get(url, params=params)
        if response.status_code != requests.codes.ok:
            raise MarketDataFetcherError(response.text)
        return response.json()

    def __make_full_url(self, endpoint: str) -> str:
        return self._financial_modeling_prep_base_url + endpoint
