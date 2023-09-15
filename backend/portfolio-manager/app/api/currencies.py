from app.components.errors import make_error_response
from app.components.currencies_manager import currencies_manager
from app.models.portfolio import currencies_schema
from flask_jwt_extended import jwt_required


@jwt_required()
def read_all():
    try:
        currencies = currencies_manager.get_currencies()
        return currencies_schema.dump(currencies), 200
    except Exception as error:
        return make_error_response(500, f"Cannot read currency entries, error: {error}")


@jwt_required()
def exchange_rates():
    try:
        return currencies_manager.get_exchange_rates()
    except Exception as error:
        return make_error_response(
            500, f"Cannot read currency exchange rates, error: {error}"
        )
