from datetime import datetime
from app.extensions import db
from app.common import make_error_response, PortmanError
from app.api.portfolios import get_portfolio_by_id
from app.models.portfolio import (
    Trade,
    TradeType,
    trade_schema,
    trades_schema,
)
from flask_jwt_extended import jwt_required


def get_trade(portfolio_id, trade_id):
    trade = db.session.scalar(db.select(Trade).filter_by(id=trade_id))
    if trade is None:
        raise PortmanError(404, f"Trade with id {trade_id} not found")
    if trade.portfolio_id is not portfolio_id:
        raise PortmanError(
            403, f"Trade with id {trade_id} does not belong to the given portfolio"
        )
    return trade


def validate_trade_params(params):
    trade_types = set(item.value for item in TradeType)
    if params["trade_type"] not in trade_types:
        raise PortmanError(400, f"Trade type '{params['trade_type']}' doesn't exist")
    try:
        datetime.strptime(params["trade_datetime"], "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError as error:
        raise PortmanError(400, f"Trade datetime is not valid, error: {error}")
    if params["unit_price"] <= 0:
        raise PortmanError(400, "Trade unit price must be a positive number")
    if params["quantity"] <= 0:
        raise PortmanError(400, "Trade quantity must be a positive number")
    if params["brokerage_fee"] < 0:
        raise PortmanError(400, "Trade brokerage fee cannot be a negative number")


@jwt_required()
def read_one(portfolio_id, trade_id):
    try:
        get_portfolio_by_id(portfolio_id)
        trade = get_trade(portfolio_id, trade_id)
        return trade_schema.dump(trade), 200
    except PortmanError as error:
        return make_error_response(error.status, error.detail)
    except Exception as error:
        db.session.rollback()
        return make_error_response(500, f"Cannot get trades, error: {error}")


@jwt_required()
def read_all(portfolio_id):
    try:
        get_portfolio_by_id(portfolio_id)
        trades = db.session.scalars(
            db.select(Trade).filter_by(portfolio_id=portfolio_id)
        )
        return trades_schema.dump(trades), 200
    except PortmanError as error:
        return make_error_response(error.status, error.detail)
    except Exception as error:
        db.session.rollback()
        return make_error_response(500, f"Cannot get trades, error: {error}")


@jwt_required()
def create(portfolio_id, trade_params):
    try:
        validate_trade_params(trade_params)
        portfolio = get_portfolio_by_id(portfolio_id)
        trade_params["portfolio_id"] = portfolio_id
        new_trade = trade_schema.load(trade_params, session=db.session)
        portfolio.trades.append(new_trade)
        db.session.commit()
        return trade_schema.dump(new_trade), 201
    except PortmanError as error:
        return make_error_response(error.status, error.detail)
    except Exception as error:
        db.session.rollback()
        return make_error_response(500, f"Cannot create a trade: {error}")


@jwt_required()
def update(portfolio_id, trade_id, trade_params):
    try:
        get_portfolio_by_id(portfolio_id)
        validate_trade_params(trade_params)
        trade_params["portfolio_id"] = portfolio_id
        new_trade = trade_schema.load(trade_params, session=db.session)
        existing_trade = get_trade(portfolio_id, trade_id)
        existing_trade.currency_id = new_trade.currency_id
        existing_trade.security_id = new_trade.security_id
        existing_trade.trade_type = new_trade.trade_type
        existing_trade.trade_datetime = new_trade.trade_datetime
        existing_trade.unit_price = new_trade.unit_price
        existing_trade.quantity = new_trade.quantity
        existing_trade.brokerage_fee = new_trade.brokerage_fee
        # db.session.merge(existing_trade)
        db.session.commit()
        return trade_schema.dump(existing_trade), 200
    except PortmanError as error:
        return make_error_response(error.status, error.detail)
    except Exception as error:
        db.session.rollback()
        return make_error_response(500, f"Cannot update a trade: {error}")


@jwt_required()
def delete(portfolio_id, trade_id):
    try:
        get_portfolio_by_id(portfolio_id)
        trade = get_trade(portfolio_id, trade_id)
        db.session.delete(trade)
        db.session.commit()
        return "", 204
    except PortmanError as error:
        return make_error_response(error.status, error.detail)
    except Exception as error:
        db.session.rollback()
        return make_error_response(500, f"Cannot delete a trade: {error}")
