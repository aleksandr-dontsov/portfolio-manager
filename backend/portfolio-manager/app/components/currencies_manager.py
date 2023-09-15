from app.components.extensions import db
from app.components.market_data_fetcher import market_data_fetcher
from app.models.portfolio import Currency


class CurrenciesManager:
    def __init__(self):
        pass

    def get_currencies(self) -> list[Currency]:
        return db.session.scalars(db.select(Currency)).all()

    def get_exchange_rates(self):
        currencies = db.session.scalars(db.select(Currency.code)).all()
        return market_data_fetcher.get_currency_exchange_rates(currencies)


currencies_manager = CurrenciesManager()
