import requests
from flask import current_app


class MarketDataFetcher:
    def init_app(self, app):
        self._base_url = app.config.get("MARKET_DATA_FETCHER_BASE_URL")

    def subscribe_for_quotes(self, securities: list[str]) -> None:
        current_app.logger.info(f"Add securities for quotes updates: {securities}")
        return self.__send_request("/market/quote", method="PUT", json=securities)

    def get_traded_securities(self):
        current_app.logger.info("Get traded securities")
        return self.__send_request("/market/security/list", method="GET")

    def make_full_url(self, route: str):
        return self._base_url + route

    def __send_request(self, endpoint: str, method, json=None):
        response = requests.request(method, self.make_full_url(endpoint), json=json)
        response.raise_for_status()
        return response.json()


market_data_fetcher = MarketDataFetcher()
