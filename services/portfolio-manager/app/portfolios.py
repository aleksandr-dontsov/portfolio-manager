from config import db
from models import Portfolio, portfolio_schema, portfolios_schema
from flask import abort, make_response

def read_all():
    # Using <Model>.query is an old interface and considered legacy in SQLAlchemy.
    # Session.execute is a preferable way
    portfolios = db.session.execute(
        db.select(Portfolio).order_by(Portfolio.name)).scalars()
    return portfolios_schema.dump(portfolios)

def read_one(portfolio_id):
    portfolio = db.session.execute(
        db.select(Portfolio).filter_by(id=portfolio_id)).scalar()
    if portfolio:
        return portfolio_schema.dump(portfolio)
    else:
        abort(404, f"Portfolio with id {portfolio_id} not found")

def create(portfolio):
    existing_portfolio = db.session.execute(
        db.select(Portfolio).filter(Portfolio.name == portfolio['name'])).first()
    if existing_portfolio is None:
        new_portfolio = portfolio_schema.load(portfolio, session=db.session)
        db.session.add(new_portfolio)
        db.session.commit()
        return portfolio_schema.dump(new_portfolio), 201
    else:
        abort(406, f"Portfolio with name {portfolio['name']} already exists")

def update(portfolio_id, portfolio):
    existing_portfolio = db.session.execute(
        db.select(Portfolio).filter_by(id=portfolio_id)).scalar()
    if existing_portfolio:
        new_portfolio = portfolio_schema.load(portfolio, session=db.session)
        existing_portfolio.name = new_portfolio.name
        existing_portfolio.currency_id = new_portfolio.currency_id
        db.session.merge(existing_portfolio)
        db.session.commit()
        return portfolio_schema.dump(existing_portfolio), 201
    else:
        abort(404, f"Portfolio with id {portfolio_id} not found")

def delete(portfolio_id):
    existing_portfolio = db.session.execute(
        db.select(Portfolio).filter_by(id=portfolio_id)).scalar()
    if existing_portfolio:
        db.session.delete(existing_portfolio)
        db.session.commit()
        return make_response(
            f"Portfolio {portfolio_id} successfully deleted", 200)
    else:
        abort(404, f"Portfolio with id {portfolio_id} not found")
