from flask import Blueprint
from app.extensions import db, se
from app.models.portfolio import Currency, Security

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

bp = Blueprint("db", __name__)
bp.cli.short_help = "Database utilities."


@bp.cli.command("init")
def init_db():
    """Initialize the database"""
    db.drop_all()
    db.create_all()


@bp.cli.command("seed")
def seed_db():
    """Seed the database"""
    se.datastore.find_or_create_role(
        name="admin",
        permissions={"admin-read", "admin-write", "user-read", "user-write"},
    )
    se.datastore.find_or_create_role(
        name="user", permissions={"user-read", "user-write"}
    )

    for currency in currencies:
        db.session.add(Currency(**currency))
    for security in securities:
        db.session.add(Security(**security))

    db.session.commit()
