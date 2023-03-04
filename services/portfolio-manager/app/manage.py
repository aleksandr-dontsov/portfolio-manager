from flask import Blueprint
from app.extensions import db, se
from app.models.portfolio import Currency

currencies = [
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
        permissions={"admin-read", "admin-write", "user-read", "user-write"})
    se.datastore.find_or_create_role(
        name="user", permissions={"user-read", "user-write"})

    for data in currencies:
        db.session.add(
            Currency(code=data["code"], name=data["name"]))

    db.session.commit()