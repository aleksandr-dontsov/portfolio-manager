from random import choice, uniform
from datetime import datetime
from config import app, db
from models import User, Currency, Portfolio, Security, Trade, TradeType

USERS = [
    {
        "email": "john.smith@gmail.com",
        "password_hash": "qwerty"
    },
    {
        "email": "bob.tailor@gmail.com",
        "password_hash": "asdfg"
    }
]

CURRENCIES = [
    {
        "code": "USD",
        "name": "Unites States dollar"
    },
    {
        "code": "EUR",
        "name": "Euro"
    },
    {
        "code": "RUB",
        "name": "Russian Ruble"
    }
]

SECURITIES = [
    {
        "isin": "US4592001014",
        "symbol": "IBM"
    },
    {
        "isin": "US88160R1014",
        "symbol": "TSLA"
    },
    {
        "isin": "US0378331005",
        "symbol": "AAPL"
    },
]

PORTFOLIO_NAMES = ("Tech companies", "Blue chips", "Retirement", "Crypto", "Cash flow")

def init_database():
    with app.app_context():
        db.drop_all()
        db.create_all()

        users = []
        for data in USERS:
            users.append(
                User(email=data["email"], password_hash=data["password_hash"]))
        
        currencies = []
        for data in CURRENCIES:
            currencies.append(
                Currency(code=data["code"], name=data["name"]))

        securities = []
        for data in SECURITIES:
            securities.append(
                Security(isin=data["isin"], symbol=data["symbol"]))

        portfolios_count = 5
        portfolios = []
        for _ in range(portfolios_count):
            portfolios.append(
                Portfolio(
                    name=choice(PORTFOLIO_NAMES),
                    user=choice(users),
                    currency=choice(currencies)))

        trades_count = 25
        for _ in range(trades_count):
            portfolio = choice(portfolios)
            db.session.add(
                Trade(
                    portfolio=portfolio,
                    currency=portfolio.currency,
                    security=choice(securities),
                    trade_type=TradeType.buy,
                    datetime=datetime.now(),
                    unit_price=round(uniform(80.00, 120.00), 2),
                    quantity=round(uniform(1.00, 5.00), 2),
                    brokerage_fee=round(uniform(0.00, 1.00), 2)))

        db.session.commit()
