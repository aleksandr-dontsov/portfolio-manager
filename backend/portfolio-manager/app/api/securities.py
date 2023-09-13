from app.components.securities_manager import securities_manager
from app.components.errors import make_error_response, PortfolioManagerError
from app.models.portfolio import securities_schema
from flask import current_app
from flask_jwt_extended import jwt_required


@jwt_required()
def search(query):
    current_app.logger.info(f"Search for securities by '{query}'")
    try:
        if securities_manager.is_update_required():
            current_app.logger.info("Securities update is needed")
            securities_manager.update_securities(securities_manager.load_securities())

        securities = securities_manager.search_securities(query)
        return securities_schema.dump(securities), 200
    except PortfolioManagerError as error:
        return make_error_response(error.status, error.detail)
    except Exception as error:
        return make_error_response(500, f"Cannot get security entries, error: {error}")
