from datetime import datetime
from flask import abort, make_response
from flask_security import auth_required, permissions_required, current_user
from app.extensions import db
from app.models.portfolio import (
    Portfolio,
    Trade,
    TradeType,
    trade_schema,
    trades_schema,
)
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException


def validate_portfolio(portfolio_id):
    portfolio = db.session.execute(
        db.select(Portfolio).filter_by(id=portfolio_id)
    ).scalar()
    if portfolio is None:
        abort(404, f"Portfolio with id {portfolio_id} not found")
    if portfolio.user_id is not current_user.id:
        abort(403)
    return portfolio


def validate_trade(portfolio_id, trade_id):
    trade = db.session.scalar(db.select(Trade).filter_by(id=trade_id))
    if trade is None:
        abort(404, f"Trade with id {trade_id} not found")
    if trade.portfolio_id is not portfolio_id:
        abort(403)
    return trade


def validate_trade_params(params):
    trade_types = set(item.value for item in TradeType)
    if params["trade_type"] not in trade_types:
        abort(400, f"Trade type '{params['trade_type']}' doesn't exist")

    try:
        datetime.strptime(params["trade_datetime"], "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError as error:
        abort(400, f"Trade datetime is not valid, error: {error}")

    if params["unit_price"] <= 0:
        abort(400, "Trade unit price must be a positive number")

    if params["quantity"] <= 0:
        abort(400, "Trade quantity must be a positive number")

    if params["brokerage_fee"] < 0:
        abort(400, "Trade brokerage fee cannot be a negative number")


@auth_required("session")
@permissions_required("user-read")
def read_all(portfolio_id):
    try:
        validate_portfolio(portfolio_id)
        trades = db.session.scalars(
            db.select(Trade).filter_by(portfolio_id=portfolio_id)
        )
        return trades_schema.dump(trades), 200
    except HTTPException:
        raise
    except Exception as error:
        abort(500, f"Cannot get trades, error: {error}")


@auth_required("session")
@permissions_required("user-write")
def create(portfolio_id, trade_params):
    try:
        validate_trade_params(trade_params)
        portfolio = validate_portfolio(portfolio_id)
        trade_params["portfolio_id"] = portfolio_id
        new_trade = trade_schema.load(trade_params, session=db.session)
        portfolio.trades.append(new_trade)
        db.session.commit()
        return trade_schema.dump(new_trade), 201
    except HTTPException:
        raise
    except SQLAlchemyError as error:
        db.session.rollback()
        abort(400, f"Cannot create a new trade entry in database: {error}")
    except Exception as error:
        abort(500, f"Cannot create a trade, error: {error}")


@auth_required("session")
@permissions_required("user-write")
def update(portfolio_id, trade_id, trade_params):
    try:
        validate_portfolio(portfolio_id)
        existing_trade = validate_trade(portfolio_id, trade_id)
        validate_trade_params(trade_params)

        trade_params["portfolio_id"] = portfolio_id
        new_trade = trade_schema.load(trade_params, session=db.session)
        existing_trade.currency_id = new_trade.currency_id
        existing_trade.security_id = new_trade.security_id
        existing_trade.trade_type = new_trade.trade_type
        existing_trade.trade_datetime = new_trade.trade_datetime
        existing_trade.unit_price = new_trade.unit_price
        existing_trade.quantity = new_trade.quantity
        existing_trade.brokerage_fee = new_trade.brokerage_fee
        db.session.merge(existing_trade)
        db.session.commit()
        return trade_schema.dump(existing_trade), 200
    except HTTPException:
        raise
    except SQLAlchemyError as error:
        db.session.rollback()
        abort(400, f"Cannot update an existing trade entry in database: {error}")
    except Exception as error:
        abort(500, f"Cannot update a trade, error: {error}")


@auth_required("session")
@permissions_required("user-write")
def delete(portfolio_id, trade_id):
    try:
        validate_portfolio(portfolio_id)
        existing_trade = validate_trade(portfolio_id, trade_id)
        db.session.delete(existing_trade)
        db.session.commit()
        return make_response(f"Trade {trade_id} successfully deleted", 200)
    except HTTPException:
        raise
    except Exception as error:
        abort(500, f"Cannot create a trade, error: {error}")
