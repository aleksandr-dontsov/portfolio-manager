from flask import Blueprint
from flask_security import hash_password
from app.extensions import db, se
from app.models.portfolio import Currency, Security

USERS = [
    {
        "email": "warren.buffet@gmail.com",
        "password": "warren"
    },
    {
        "email": "george.soros@gmail.com",
        "password": "george"
    },
    {
        "email": "benjamin.graham@gmail.com",
        "password": "benjamin"
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

bp = Blueprint("db", __name__)
bp.cli.short_help = "Database utilities."

@bp.cli.command("init")
def init_db():
    """Initialize the database"""
    db.drop_all()
    db.create_all()
    db.session.commit()

@bp.cli.command("seed")
def seed_db():
    """Seed the database"""
    se.datastore.find_or_create_role(
        name="admin",
        permissions={"admin-read", "admin-write", "user-read", "user-write"})
    se.datastore.find_or_create_role(
        name="user", permissions={"user-read", "user-write"})

    for data in USERS:
        se.datastore.create_user(
            email=data["email"], password=hash_password(data["password"]), roles=["user"])

    currencies = []
    for data in CURRENCIES:
        currencies.append(
            Currency(code=data["code"], name=data["name"]))

    securities = []
    for data in SECURITIES:
        securities.append(
            Security(isin=data["isin"], symbol=data["symbol"]))

    db.session.add_all(currencies)
    db.session.add_all(securities)
    db.session.commit()