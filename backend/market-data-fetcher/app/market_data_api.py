from alpha_vantage.alphavantage import AlphaVantage as av
from datetime import date


class MarketDataApi(av):
    def __init__(self, app):
        super(MarketDataApi, self).__init__(
            key=app.config.get("ALPHA_VANTAGE_API_KEY"), output_format="csv"
        )

    # def get_listing_status(self, date = date.today(), status = 'active'):
    @av._output_format
    @av._call_api_on_func
    def get_listing_status(self, date=date.today(), state="active"):
        _FUNCTION_KEY = "LISTING_STATUS"
        return _FUNCTION_KEY, "date", "state"
