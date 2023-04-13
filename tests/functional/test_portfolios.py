"""
This file (test_portfolios.py) contains the functional tests for the portfolios views.

These tests use GET/POST/PUT/DELETE methods to different URLs to check for the proper
behavior of the portfolios views.
"""

import pytest
from flask_security import current_user
from sqlalchemy import func
from conftest import existing_portfolio, new_portfolio
from app.extensions import db
from app.models.portfolio import Portfolio, portfolio_schema


def test_unauthenticated_read_all(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios' page is requested (GET) when the user isn't logged in
    THEN check that an error response is returned to the user
    """
    response = test_client.get("/api/portfolios")
    assert response.status_code == 401


def test_successful_read_all(test_client, login_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios' page is requested (GET) when the user is logged in
    THEN check that the response is successful and that the empty list is returned
    """
    response = test_client.get("/api/portfolios")
    assert response.status_code == 200
    portfolios = response.json
    assert not portfolios


def test_unauthenticated_create(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios' page is posted to (POST) when the user isn't logged in
    THEN check that an error response is returned to the user
    """
    response = test_client.post("/api/portfolios", json=new_portfolio)
    assert response.status_code == 401


@pytest.mark.parametrize(
    "portfolio",
    [
        {"name": "Test", "currency_id": -1},
        {"name": "AnotherTest", "currency_id": 9999},
        {"name": "", "currency_id": 1},
        {"name": "Too long portfolio name" * 50, "currency_id": 1},
    ],
)
def test_invalid_portfolio_create(test_client, login_user, portfolio):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios' page is posted to (POST) when the user is logged in
         and invalid portfolio params are passed
    THEN check that an error response is returned to the user
    """
    response = test_client.post("/api/portfolios", json=portfolio)
    assert response.status_code == 400
    assert db.session.execute(func.count(Portfolio.id)).scalar() == 0


def test_successful_portfolio_create(test_client, login_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios' page is posted to (POST) when the user is logged in
    THEN check that the response is successful and
         that the portfolio has been inserted in the database for a default user
    """
    response = test_client.post("/api/portfolios", json=new_portfolio)
    assert response.status_code == 201
    portfolio = response.json
    assert portfolio["name"] == new_portfolio["name"]
    assert portfolio["currency_id"] == new_portfolio["currency_id"]
    assert len(portfolio["trades"]) == 0
    assert portfolio["user_id"] == current_user.id

    portfolios = db.session.execute(
        db.select(Portfolio).filter_by(name=new_portfolio["name"])
    ).scalars()
    assert portfolio_schema.dump(portfolios.one()) == portfolio


def test_duplicate_portfolio_create(test_client, create_portfolio):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios' page is posted to (POST) when the user is logged in
         and the portfolio with a given name exists
    THEN check that an error response is returned to the user
    """
    response = test_client.post("/api/portfolios", json=existing_portfolio)
    assert response.status_code == 400


def test_unauthenticated_read_one(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios/{portfolio_id}' page is requested (GET) when the user isn't logged in
    THEN check that an error response is returned to the user
    """
    response = test_client.get("/api/portfolios/1")
    assert response.status_code == 401


def test_invalid_portfolio_id_param_read_one(test_client, login_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios/{portfolio_id}' page is requested (GET)
         when the portfolio with a given id doesn't exist
    THEN check that an error response is returned to the user
    """
    response = test_client.get("/api/portfolios/string")
    assert response.status_code == 404


def test_nonexistent_read_one(test_client, login_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios/{portfolio_id}' page is requested (GET)
         when the portfolio with a given id doesn't exist
    THEN check that an error response is returned to the user
    """
    response = test_client.get("/api/portfolios/999")
    assert response.status_code == 404


def test_unauthorized_portfolio_read_one(
    test_client, login_user, create_new_user_portfolio
):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios/{portfolio_id}' page is put to (PUT) when
         the portfolio with a given id belongs to other user
    THEN check that an error response is returned to the user
    """

    response = test_client.put("/api/portfolios/1", json=new_portfolio)
    assert response.status_code == 403


def test_successful_read_one(test_client, create_portfolio):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios' page is posted to (POST) when the user is logged in
    THEN check that the response is successful and
         that the portfolio has been inserted in the database for a default user
    """
    response = test_client.get("/api/portfolios/1")
    assert response.status_code == 200
    portfolio = response.json
    assert portfolio["id"] == 1
    assert portfolio["user_id"] == current_user.id


def test_unauthenticated_update(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios/{portfolio_id}' page is put to (PUT) when the user isn't logged in
    THEN check that an error response is returned to the user
    """
    response = test_client.put("/api/portfolios/1", json=new_portfolio)
    assert response.status_code == 401


@pytest.mark.parametrize(
    "portfolio",
    [
        {"name": "Test", "currency_id": -1},
        {"name": "", "currency_id": 1},
        {"name": "Too long portfolio name" * 50, "currency_id": 1},
    ],
)
def test_invalid_portfolio_update(test_client, create_portfolio, portfolio):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios' page is put to (PUT) when the user is logged in
         and invalid portfolio data is passed
    THEN check that an error response is returned to the user
    """
    response = test_client.put("/api/portfolios/1", json=portfolio)
    assert response.status_code == 400


def test_nonexistent_portfolio_update(test_client, create_portfolio):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios/{portfolio_id}' page is put to (PUT)
         when the portfolio with a given id doesn't exist
    THEN check that an error response is returned to the user
    """
    response = test_client.put("/api/portfolios/999", json=new_portfolio)
    assert response.status_code == 404


def test_unauthorized_portfolio_update(
    test_client, login_user, create_new_user_portfolio
):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios/{portfolio_id}' page is put to (PUT) when
         the portfolio with a given id belongs to other user
    THEN check that an error response is returned to the user
    """

    response = test_client.put("/api/portfolios/1", json=new_portfolio)
    assert response.status_code == 403


def test_successful_portfolio_update(test_client, create_portfolio):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios/{portfolio_id}' page is put to (PUT) when the user is logged in
    THEN check that the response is successful and
         that the portfolio has been updated in the database
    """

    response = test_client.put("/api/portfolios/1", json=new_portfolio)
    assert response.status_code == 200
    portfolio = response.json
    assert portfolio["id"] == 1
    assert portfolio["updated_at"] > portfolio["created_at"]
    assert portfolio["user_id"] == current_user.id
    assert portfolio["name"] == new_portfolio["name"]
    assert portfolio["currency_id"] == new_portfolio["currency_id"]


def test_unauthenticated_portfolio_delete(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios/{portfolio_id}' page is requested (DELETE) when the user isn't logged in
    THEN check that an error response is returned to the user
    """
    response = test_client.delete("/api/portfolios/1")
    assert response.status_code == 401


def test_nonexistent_portfolio_delete(test_client, login_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios/{portfolio_id}' page is requested (DELETE)
         when the portfolio with a given id doesn't exist
    THEN check that an error response is returned to the user
    """
    response = test_client.delete("/api/portfolios/999")
    assert response.status_code == 404


def test_unauthorized_portfolio_delete(
    test_client, login_user, create_new_user_portfolio
):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios/{portfolio_id}' page is requested (DELETE) when
         the portfolio with a given id belongs to other user
    THEN check that an error response is returned to the user
    """
    response = test_client.delete("/api/portfolios/1")
    assert response.status_code == 403


def test_successful_portfolio_delete(test_client, create_portfolio):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios/{portfolio_id}' page is requested (DELETE) when
         the portfolio belongs to the current logged in user
    THEN check that the response is successful and
         that the portfolio has been removed from the database
    """
    response = test_client.delete("/api/portfolios/1")
    assert response.status_code == 200

    portfolios = db.session.execute(db.select(Portfolio).filter_by(id=1)).scalar()
    assert portfolios is None
