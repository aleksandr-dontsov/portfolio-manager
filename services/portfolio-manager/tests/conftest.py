import pytest
from random import uniform, randint, choice
from datetime import datetime, timezone
from flask_security import current_user

from app import create_app
from app.config import TestingConfig
from app.extensions import db, se
from app.models.portfolio import Currency, Portfolio, Security, Trade

registered_user = {"email": "registered.user@gmail.com", "password": "Registered.user1"}
new_user = {"email": "new.user@gmail.com", "password": "New.user2"}
currencies = [
    {"code": "USD", "name": "Unites States dollar"},
    {"code": "EUR", "name": "Euro"},
    {"code": "RUB", "name": "Russian Ruble"},
]

securities = [
    {"isin": "US4592001014", "symbol": "IBM"},
    {"isin": "US88160R1014", "symbol": "TSLA"},
    {"isin": "US0378331005", "symbol": "AAPL"},
]

existing_portfolio = {"name": "Existing portfolio", "currency_id": 1}
new_portfolio = {"name": "New portfolio", "currency_id": 2}

existing_trade = {
    "portfolio_id": 1,
    "currency_id": 1,
    "security_id": 1,
    "trade_type": "buy",
    "trade_datetime": datetime.now(timezone.utc).replace(tzinfo=None),
    "unit_price": 99.99,
    "quantity": 2.50,
    "brokerage_fee": 1.25,
}

EXISTING_TRADES_NUMBER = 5


@pytest.fixture(scope="module")
def app():
    yield create_app(TestingConfig)


@pytest.fixture(scope="module")
def test_client(app):
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture(scope="module")
def test_runner(app):
    return app.test_cli_runner()


@pytest.fixture(scope="function")
def init_database(test_client):
    # Create the database and the database tables
    db.create_all()

    # Create roles
    se.datastore.find_or_create_role(
        name="admin",
        permissions={"admin-read", "admin-write", "user-read", "user-write"},
    )
    se.datastore.find_or_create_role(
        name="user", permissions={"user-read", "user-write"}
    )

    # Create currencies
    for currency in currencies:
        db.session.add(Currency(**currency))

    # Create securities
    for security in securities:
        db.session.add(Security(**security))

    db.session.commit()

    # This is where the testing happens
    yield

    # Explicitly close database connection
    db.session.close()

    db.drop_all()


@pytest.fixture(scope="function")
def register_user(init_database):
    se.datastore.create_user(**registered_user, roles=["user"])


@pytest.fixture(scope="function")
def login_user(register_user, test_client):
    test_client.post("/api/login", json=registered_user)

    # This is where the testing happens
    yield
    test_client.post("/api/logout")


@pytest.fixture(scope="function")
def create_portfolio(login_user):
    db.session.add(Portfolio(**existing_portfolio, user_id=current_user.id))
    db.session.commit()


@pytest.fixture(scope="function")
def create_new_user_portfolio(test_client):
    user = se.datastore.create_user(**new_user, roles=["user"])
    db.session.add(Portfolio(**new_portfolio, user=user))
    db.session.commit()


def create_random_trade_params():
    return {
        "currency_id": randint(1, len(currencies)),
        "security_id": randint(1, len(securities)),
        "trade_type": choice(["buy", "sell"]),
        "trade_datetime": datetime.now(timezone.utc).replace(tzinfo=None),
        "unit_price": round(uniform(80.00, 120.00), 2),
        "quantity": round(uniform(1.00, 5.00), 2),
        "brokerage_fee": round(uniform(0.00, 1.00), 2),
    }


@pytest.fixture(scope="function")
def create_trade(create_portfolio):
    db.session.add(Trade(**existing_trade))
    db.session.commit()


@pytest.fixture(scope="function")
def create_random_trades(create_portfolio):
    for _ in range(EXISTING_TRADES_NUMBER):
        db.session.add(Trade(portfolio_id=1, **create_random_trade_params()))
    db.session.commit()
