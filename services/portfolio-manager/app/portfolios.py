from config import db
from models import Portfolio, portfolio_schema, portfolios_schema
from flask import abort, make_response
from flask_security import (
    auth_required,
    permissions_required,
    current_user
)

@auth_required("session")
@permissions_required("user-read")
def read_all():
    # Using <Model>.query is an old interface and considered legacy in SQLAlchemy.
    # Session.execute is a preferable way
    portfolios = db.session.execute(
        db.select(Portfolio).filter_by(user_id=current_user.id).order_by(Portfolio.name)).scalars()
    return portfolios_schema.dump(portfolios)

@auth_required("session")
@permissions_required("user-read")
def read_one(portfolio_id):
    portfolio = db.session.execute(
        db.select(Portfolio).filter_by(id=portfolio_id)).scalar()

    if portfolio is None:
        abort(404, f"Portfolio with id {portfolio_id} not found")

    if portfolio.user_id is not current_user.id:
        abort(403)

    return portfolio_schema.dump(portfolio)

@auth_required("session")
@permissions_required("user-write")
def create(portfolio):
    existing_portfolio = db.session.execute(
        db.select(Portfolio).filter_by(user_id=current_user.id, name=portfolio['name'])).scalar()

    if existing_portfolio is not None:
        abort(406, f"Portfolio with name {portfolio['name']} already exists")

    portfolio['user_id'] = current_user.id
    new_portfolio = portfolio_schema.load(portfolio, session=db.session)
    db.session.add(new_portfolio)
    db.session.commit()
    return portfolio_schema.dump(new_portfolio), 201

@auth_required("session")
@permissions_required("user-write")
def update(portfolio_id, portfolio):
    existing_portfolio = db.session.execute(
        db.select(Portfolio).filter_by(id=portfolio_id)).scalar()

    if existing_portfolio is None:
        abort(404, f"Portfolio with id {portfolio_id} not found")

    if existing_portfolio.user_id is not current_user.id:
        abort(403)

    new_portfolio = portfolio_schema.load(portfolio, session=db.session)
    existing_portfolio.name = new_portfolio.name
    existing_portfolio.currency_id = new_portfolio.currency_id
    db.session.merge(existing_portfolio)
    db.session.commit()
    return portfolio_schema.dump(existing_portfolio), 201

@auth_required("session")
@permissions_required("user-write")
def delete(portfolio_id):
    existing_portfolio = db.session.execute(
        db.select(Portfolio).filter_by(id=portfolio_id)).scalar()

    if existing_portfolio is None:
        abort(404, f"Portfolio with id {portfolio_id} not found")

    if existing_portfolio.user_id is not current_user.id:
        abort(403)

    db.session.delete(existing_portfolio)
    db.session.commit()
    return make_response(f"Portfolio {portfolio_id} successfully deleted", 200)