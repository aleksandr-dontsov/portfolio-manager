from random import choice, uniform
from datetime import datetime
from flask.cli import FlaskGroup
from flask_security import hash_password
from config import app, db
from models import (
    User,
    Currency,
    Portfolio,
    Security,
    Trade,
    TradeType
)

USERS = [
    {
        "email": "test1@test1.com",
        "password": "test1"
    },
    {
        "email": "test2@test2.com",
        "password": "test2"
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

cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def seed_db():
    with app.app_context():
        app.security.datastore.find_or_create_role(
            name="admin",
            permissions={"admin-read", "admin-write", "user-read", "user-write"})
        app.security.datastore.find_or_create_role(
            name="user", permissions={"user-read", "user-write"})

        for data in USERS:
            app.security.datastore.create_user(
                email=data["email"], password=hash_password(data["password"]))

        currencies = []
        for data in CURRENCIES:
            currencies.append(
                Currency(code=data["code"], name=data["name"]))

        securities = []
        for data in SECURITIES:
            securities.append(
                Security(isin=data["isin"], symbol=data["symbol"]))

        # portfolios_count = 5
        # portfolios = []
        # for _ in range(portfolios_count):
        #     portfolios.append(
        #         Portfolio(
        #             name=choice(PORTFOLIO_NAMES),
        #             user=choice(users),
        #             currency=choice(currencies)))

        # trades_count = 25
        # for _ in range(trades_count):
        #     portfolio = choice(portfolios)
        #     db.session.add(
        #         Trade(portfolio=portfolio,
        #               currency=portfolio.currency,
        #               security=choice(securities),
        #               trade_type=TradeType.buy,
        #               datetime=datetime.now(),
        #               unit_price=round(uniform(80.00, 120.00), 2),
        #               quantity=round(uniform(1.00, 5.00), 2),
        #               brokerage_fee=round(uniform(0.00, 1.00), 2)))

        db.session.add_all(currencies)
        db.session.add_all(securities)
        db.session.commit()

if __name__ == "__main__":
    cli()