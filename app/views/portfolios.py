from flask import abort, make_response
from flask_security import auth_required, permissions_required, current_user
from app.extensions import db
from app.models.portfolio import Portfolio, portfolio_schema, portfolios_schema
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException

MAX_PORTFOLIO_NAME_LENGTH = 150


def validate_portfolio_params(portfolio):
    if not portfolio["name"]:
        abort(400, "Portfolio name is empty")

    if len(portfolio["name"]) > MAX_PORTFOLIO_NAME_LENGTH:
        abort(
            400,
            f"Portfolio name length is more than {MAX_PORTFOLIO_NAME_LENGTH} characters",
        )

    if portfolio["currency_id"] < 1:
        abort(400, "Specified currency doesn't exist")


def validate_portfolio(portfolio_id):
    portfolio = db.one_or_404(db.select(Portfolio).filter_by(id=portfolio_id))
    if portfolio.user_id is not current_user.id:
        abort(403)

    return portfolio


@auth_required("session")
@permissions_required("user-read")
def read_all():
    # Using <Model>.query is an old interface and considered legacy in SQLAlchemy.
    # Session.execute is a preferable way
    try:
        portfolios = db.session.execute(
            db.select(Portfolio)
            .filter_by(user_id=current_user.id)
            .order_by(Portfolio.name)
        ).scalars()
        return portfolios_schema.dump(portfolios), 200
    except Exception as error:
        abort(500, f"Cannot get portfolio entries, error: {error}")


@auth_required("session")
@permissions_required("user-read")
def read_one(portfolio_id):
    try:
        portfolio = db.one_or_404(db.select(Portfolio).filter_by(id=portfolio_id))
        if portfolio.user_id is not current_user.id:
            abort(403)
        return portfolio_schema.dump(portfolio), 200
    except HTTPException:
        raise
    except Exception as error:
        abort(500, f"Cannot get a given portfolio entry, error: {error}")


@auth_required("session")
@permissions_required("user-write")
def create(portfolio):
    try:
        validate_portfolio_params(portfolio)
        existing_portfolio = db.session.execute(
            db.select(Portfolio).filter_by(
                user_id=current_user.id, name=portfolio["name"]
            )
        ).scalar()
        if existing_portfolio is not None:
            abort(400, f"Portfolio with name {portfolio['name']} already exists")
        portfolio["user_id"] = current_user.id
        new_portfolio = portfolio_schema.load(portfolio, session=db.session)
        db.session.add(new_portfolio)
        db.session.commit()
        return portfolio_schema.dump(new_portfolio), 201
    except HTTPException:
        raise
    except SQLAlchemyError as error:
        db.session.rollback()
        abort(400, f"Cannot create a new portfolio entry in database: {error}")
    except Exception as error:
        abort(500, f"Cannot update a portfolio entry, error: {error}")


@auth_required("session")
@permissions_required("user-write")
def update(portfolio_id, portfolio):
    try:
        validate_portfolio_params(portfolio)
        existing_portfolio = validate_portfolio(portfolio_id)
        portfolio["user_id"] = current_user.id
        new_portfolio = portfolio_schema.load(portfolio, session=db.session)
        existing_portfolio.name = new_portfolio.name
        existing_portfolio.currency_id = new_portfolio.currency_id
        db.session.merge(existing_portfolio)
        db.session.commit()
        return portfolio_schema.dump(existing_portfolio), 200
    except HTTPException:
        raise
    except SQLAlchemyError as error:
        db.session.rollback()
        abort(400, f"Cannot update an existing portfolio entry in database: {error}")
    except Exception as error:
        abort(500, f"Cannot update a portfolio entry, error: {error}")


@auth_required("session")
@permissions_required("user-write")
def delete(portfolio_id):
    try:
        existing_portfolio = validate_portfolio(portfolio_id)
        db.session.delete(existing_portfolio)
        db.session.commit()
        return make_response(f"Portfolio {portfolio_id} successfully deleted", 200)
    except HTTPException:
        raise
    except Exception as error:
        abort(500, f"Cannot delete a portfolio entry, error: {error}")
