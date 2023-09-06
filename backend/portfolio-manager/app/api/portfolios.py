from app.components.extensions import db
from app.components.errors import make_error_response, PortfolioManagerError
from app.models.portfolio import Portfolio, portfolio_schema, portfolios_schema
from flask_jwt_extended import get_current_user, jwt_required
from sqlalchemy import asc

MAX_PORTFOLIO_NAME_LENGTH = 150


def validate_portfolio_params(portfolio):
    if not portfolio["name"]:
        raise PortfolioManagerError(400, "Portfolio name is empty")
    if len(portfolio["name"]) > MAX_PORTFOLIO_NAME_LENGTH:
        raise PortfolioManagerError(
            400,
            f"Portfolio name length is more than {MAX_PORTFOLIO_NAME_LENGTH} characters",
        )
    if portfolio["currency_id"] < 1:
        raise PortfolioManagerError(
            400, f"Currency with id {portfolio['currency_id']} doesn't exist"
        )


def get_portfolio_by_id(portfolio_id):
    portfolio = db.session.execute(
        db.select(Portfolio).filter_by(id=portfolio_id)
    ).scalar()
    if not portfolio:
        raise PortfolioManagerError(404, f"Portfolio with id {portfolio_id} not found")
    if portfolio.user_id != get_current_user().id:
        raise PortfolioManagerError(
            403, f"Portfolio with id {portfolio_id} doesn't belong to the current user"
        )
    return portfolio


def get_portfolio_by_name(portfolio_name):
    user_id = get_current_user().id
    portfolio = db.session.execute(
        db.select(Portfolio).filter_by(user_id=user_id, name=portfolio_name)
    ).scalar()
    if not portfolio:
        raise PortfolioManagerError(
            404, f"Portfolio with name '{portfolio_name}' not found"
        )
    return portfolio


@jwt_required()
def read_all():
    # Using <Model>.query is an old interface and considered legacy in SQLAlchemy.
    # Session.execute is a preferable way
    try:
        current_user = get_current_user()
        portfolios = db.session.execute(
            db.select(Portfolio)
            .filter_by(user_id=current_user.id)
            .order_by(asc(Portfolio.created_at))
        ).scalars()
        return portfolios_schema.dump(portfolios), 200
    except Exception as error:
        db.session.rollback()
        return make_error_response(500, f"Cannot get portfolio entries, error: {error}")


@jwt_required()
def read_one(portfolio_id):
    try:
        return portfolio_schema.dump(get_portfolio_by_id(portfolio_id)), 200
    except PortfolioManagerError as error:
        return make_error_response(error.status, error.detail)
    except Exception as error:
        db.session.rollback()
        return make_error_response(
            500, f"Cannot read a given portfolio with id {portfolio_id}, error: {error}"
        )


@jwt_required()
def create(portfolio):
    try:
        current_user = get_current_user()
        validate_portfolio_params(portfolio)
        existing_portfolio = db.session.execute(
            db.select(Portfolio).filter_by(
                user_id=current_user.id, name=portfolio["name"]
            )
        ).scalar()
        if existing_portfolio:
            raise PortfolioManagerError(
                400, f"Portfolio with a name '{portfolio['name']}' already exists"
            )
        portfolio["user_id"] = current_user.id
        new_portfolio = portfolio_schema.load(portfolio, session=db.session)
        db.session.add(new_portfolio)
        db.session.commit()
        return portfolio_schema.dump(new_portfolio), 201
    except PortfolioManagerError as error:
        return make_error_response(error.status, error.detail)
    except Exception as error:
        db.session.rollback()
        make_error_response(500, f"Cannot create a portfolio entry: {error}")


@jwt_required()
def update(portfolio_id, portfolio):
    try:
        current_user = get_current_user()
        validate_portfolio_params(portfolio)
        updated_portfolio = get_portfolio_by_id(portfolio_id)
        existing_portfolio = db.session.execute(
            db.select(Portfolio).filter_by(
                user_id=current_user.id, name=portfolio["name"]
            )
        ).scalar()
        if existing_portfolio and existing_portfolio.id != portfolio_id:
            raise PortfolioManagerError(
                400, f"Portfolio with a name '{portfolio['name']}' already exists"
            )

        portfolio["user_id"] = current_user.id
        new_portfolio = portfolio_schema.load(portfolio, session=db.session)
        updated_portfolio.name = new_portfolio.name
        updated_portfolio.currency_id = new_portfolio.currency_id
        db.session.commit()
        return portfolio_schema.dump(updated_portfolio), 200
    except PortfolioManagerError as error:
        return make_error_response(error.status, error.detail)
    except Exception as error:
        db.session.rollback()
        make_error_response(500, f"Cannot update a portfolio entry: {error}")


@jwt_required()
def delete(portfolio_id):
    try:
        portfolio = get_portfolio_by_id(portfolio_id)
        db.session.delete(portfolio)
        db.session.commit()
        return "", 204
    except PortfolioManagerError as error:
        return make_error_response(error.status, error.detail)
    except Exception as error:
        db.session.rollback()
        make_error_response(500, f"Cannot delete a portfolio entry: {error}")
