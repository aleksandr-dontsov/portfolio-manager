from app.components.extensions import db
from app.components.errors import make_error_response
from app.models.portfolio import Currency, currencies_schema
from flask_jwt_extended import jwt_required


@jwt_required()
def read_all():
    try:
        currencies = db.session.execute(db.select(Currency)).scalars()
        return currencies_schema.dump(currencies), 200
    except Exception as error:
        db.session.rollback()
        return make_error_response(500, f"Cannot read currency entries, error: {error}")
