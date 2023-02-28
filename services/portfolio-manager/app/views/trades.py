from flask import abort, make_response
from flask_security import (
    auth_required,
    permissions_required,
    current_user
)
from app.extensions import db
from app.models.portfolio import (
    Portfolio,
    Trade,
    trade_schema,
    trades_schema
)

@auth_required("session")
@permissions_required("user-read")
def read_all(portfolio_id):
    portfolio = db.session.execute(
        db.select(Portfolio).filter_by(id=portfolio_id)).scalar()
    if portfolio is None:
        abort(404, f"Portfolio with id {portfolio_id} not found")
    if portfolio.user_id is not current_user.id:
        abort(403)
    trades = db.session.scalars(
        db.select(Trade).filter_by(portfolio_id=portfolio_id))
    return trades_schema.dump(trades)

@auth_required("session")
@permissions_required("user-write")
def create(portfolio_id, trade):
    portfolio = db.session.scalar(
        db.select(Portfolio).filter_by(id=portfolio_id))
    if portfolio is None:
        abort(404, f"Portfolio with id {portfolio_id} not found")
    if portfolio.user_id is not current_user.id:
        abort(403)

    trade['portfolio_id'] = portfolio_id
    new_trade = trade_schema.load(trade, session=db.session)
    portfolio.trades.append(new_trade)
    db.session.commit()
    return trade_schema.dump(new_trade), 201

@auth_required("session")
@permissions_required("user-write")
def update(portfolio_id, trade_id, trade):
    portfolio = db.session.scalar(
        db.select(Portfolio).filter_by(id=portfolio_id))
    if portfolio is None:
        abort(404, f"Portfolio with id {portfolio_id} not found")
    if portfolio.user_id is not current_user.id:
        abort(403)

    existing_trade = db.session.scalar(
        db.select(Trade).filter_by(id=trade_id))
    if existing_trade is None:
        abort(404, f"Trade with id {trade_id} not found")
    if existing_trade.portfolio_id is not portfolio_id:
        abort(403)

    trade['portfolio_id'] = portfolio_id
    new_trade = trade_schema.load(trade, session=db.session)
    existing_trade.currency_id = new_trade.currency_id
    existing_trade.security_id = new_trade.security_id
    existing_trade.trade_type = new_trade.trade_type
    existing_trade.datetime = new_trade.datetime
    existing_trade.unit_price = new_trade.unit_price
    existing_trade.quantity = new_trade.quantity
    existing_trade.brokerage_fee = new_trade.brokerage_fee
    db.session.merge(existing_trade)
    db.session.commit()
    return trade_schema.dump(existing_trade), 201

@auth_required("session")
@permissions_required("user-write")
def delete(portfolio_id, trade_id):
    portfolio = db.session.scalar(
        db.select(Portfolio).filter_by(id=portfolio_id))
    if portfolio is None:
        abort(404, f"Portfolio with id {portfolio_id} not found")
    if portfolio.user_id is not current_user.id:
        abort(403)

    existing_trade = db.session.scalar(
        db.select(Trade).filter_by(id=trade_id))
    if existing_trade is None:
        abort(404, f"Trade with id {trade_id} not found")
    if existing_trade.portfolio_id is not portfolio_id:
        abort(403)

    db.session.delete(existing_trade)
    db.session.commit()
    return make_response(
        f"Trade {trade_id} successfully deleted", 200)