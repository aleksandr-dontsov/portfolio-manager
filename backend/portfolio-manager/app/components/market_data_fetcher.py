import requests
from flask import current_app


class MarketDataFetcher:
    def init_app(self, app):
        self._base_url = app.config.get("MARKET_DATA_FETCHER_BASE_URL")

    def subscribe_for_quotes(self, securities: list[str]):
        current_app.logger.info(f"Add securities for quotes updates: {securities}")
        return self.__send_request("/market/quote", method="POST", json=securities)

    def get_traded_securities(self):
        current_app.logger.info("Get traded securities")
        return self.__send_request("/market/securities", method="GET")

    def get_currency_exchange_rates(self, currencies: list[str]):
        current_app.logger.info("Get currency exchange rates")
        return self.__send_request(
            "/market/fx", method="GET", params={"currencies": ",".join(currencies)}
        )

    def make_full_url(self, route: str):
        return self._base_url + route

    def __send_request(self, endpoint: str, method, json=None, params=None):
        response = requests.request(
            method, self.make_full_url(endpoint), json=json, params=params
        )
        response.raise_for_status()
        return response.json()


market_data_fetcher = MarketDataFetcher()
