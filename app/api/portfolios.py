from flask_security import auth_required, permissions_required, current_user
from app.extensions import db
from app.common import make_error_response, PortmanError
from app.models.portfolio import Portfolio, portfolio_schema, portfolios_schema

MAX_PORTFOLIO_NAME_LENGTH = 150


def validate_portfolio_params(portfolio):
    if not portfolio["name"]:
        raise PortmanError(400, "Portfolio name is empty")
    if len(portfolio["name"]) > MAX_PORTFOLIO_NAME_LENGTH:
        raise PortmanError(
            400,
            f"Portfolio name length is more than {MAX_PORTFOLIO_NAME_LENGTH} characters",
        )
    if portfolio["currency_id"] < 1:
        raise PortmanError(
            400, f"Currency with id {portfolio['currency_id']} doesn't exist"
        )


def get_portfolio(portfolio_id):
    portfolio = db.session.execute(
        db.select(Portfolio).filter_by(id=portfolio_id)
    ).scalar()
    if not portfolio:
        raise PortmanError(404, f"Portfolio with id {portfolio_id} not found")
    if portfolio.user_id is not current_user.id:
        raise PortmanError(
            403, f"Portfolio with id {portfolio_id} does not belong to the given user"
        )
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
        db.session.rollback()
        return make_error_response(500, f"Cannot get portfolio entries, error: {error}")


@auth_required("session")
@permissions_required("user-read")
def read_one(portfolio_id):
    try:
        return portfolio_schema.dump(get_portfolio(portfolio_id)), 200
    except PortmanError as error:
        return make_error_response(error.status, error.detail)
    except Exception as error:
        db.session.rollback()
        return make_error_response(
            500, f"Cannot read a given portfolio with id {portfolio_id}, error: {error}"
        )


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
        if existing_portfolio:
            raise PortmanError(
                400, f"Portfolio with a name '{portfolio['name']}' already exists"
            )
        portfolio["user_id"] = current_user.id
        new_portfolio = portfolio_schema.load(portfolio, session=db.session)
        db.session.add(new_portfolio)
        db.session.commit()
        return portfolio_schema.dump(new_portfolio), 201
    except PortmanError as error:
        return make_error_response(error.status, error.detail)
    except Exception as error:
        db.session.rollback()
        make_error_response(500, f"Cannot create a portfolio entry: {error}")


@auth_required("session")
@permissions_required("user-write")
def update(portfolio_id, portfolio):
    try:
        validate_portfolio_params(portfolio)
        portfolio["user_id"] = current_user.id
        new_portfolio = portfolio_schema.load(portfolio, session=db.session)
        existing_portfolio = get_portfolio(portfolio_id)
        existing_portfolio.name = new_portfolio.name
        existing_portfolio.currency_id = new_portfolio.currency_id
        db.session.commit()
        return portfolio_schema.dump(existing_portfolio), 200
    except PortmanError as error:
        return make_error_response(error.status, error.detail)
    except Exception as error:
        db.session.rollback()
        make_error_response(500, f"Cannot update a portfolio entry: {error}")


@auth_required("session")
@permissions_required("user-write")
def delete(portfolio_id):
    try:
        portfolio = get_portfolio(portfolio_id)
        db.session.delete(portfolio)
        db.session.commit()
        return "", 204
    except PortmanError as error:
        return make_error_response(error.status, error.detail)
    except Exception as error:
        db.session.rollback()
        make_error_response(500, f"Cannot delete a portfolio entry: {error}")
