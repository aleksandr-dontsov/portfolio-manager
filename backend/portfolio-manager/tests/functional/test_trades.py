"""
This file (test_portfolios.py) contains the functional tests for the portfolios views.

These tests use GET/POST/PUT/DELETE methods to different URLs to check for the proper
behavior of the trades views.
"""

import pytest
from datetime import datetime
from sqlalchemy import func
from conftest import existing_trade, create_random_trade_params
from app.components.extensions import db
from app.models.portfolio import Trade


def test_unauthenticated_trades_read_all(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios/1/trades' page is requested (GET) when the user isn't logged in
    THEN check that an error response is returned to the user
    """
    response = test_client.get("/api/portfolios/1/trades")
    assert response.status_code == 401


def test_unauthorized_trades_read_all(
    test_client, login_user, create_new_user_portfolio
):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios/{portfolio_id}/trades' page is requested (GET)
         when the user is logged in and
         the portfolio with a given id belongs to other user
    THEN check that an error response is returned to the user
    """

    response = test_client.get("/api/portfolios/1/trades")
    assert response.status_code == 403


def test_successful_read_all(test_client, create_trade):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/portfolios/{portfolio_id}/trades'
         page is requested (GET) when the user is logged in
    THEN check that the response is successful and that the empty list is returned
    """
    response = test_client.get("/api/portfolios/1/trades")
    assert response.status_code == 200
    trades = response.json
    assert len(trades) == 1


def test_unauthenticated_trade_create(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios/{portfolio_id}/trades'
         page is posted to (POST) when the user isn't logged in
    THEN check that an error response is returned to the user
    """
    response = test_client.post(
        "/api/portfolios/1/trades", json=create_random_trade_params()
    )
    assert response.status_code == 401


def test_unauthorized_trade_create(test_client, login_user, create_new_user_portfolio):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios/{portfolio_id}/trades' page is posted to (POST)
         when the user is logged in and the portfolio with a given id belongs to other user
    THEN check that an error response is returned to the user
    """
    response = test_client.post(
        "/api/portfolios/1/trades", json=create_random_trade_params()
    )
    assert response.status_code == 403


@pytest.mark.parametrize(
    "invalid_trade_params",
    [
        {
            "currency_id": -1,
        },
        {
            "currency_id": 9999,
        },
        {
            "security_id": -1,
        },
        {
            "security_id": 9999,
        },
        {
            "trade_type": "invalid trade type",
        },
        {
            "trade_datetime": "it's not a datetime",
        },
        {
            "unit_price": -9.999,
        },
        {
            "unit_price": 0,
        },
        {
            "quantity": -10,
        },
        {
            "quantity": 0,
        },
        {
            "brokerage_fee": -9.999,
        },
    ],
)
def test_invalid_trade_create(test_client, create_portfolio, invalid_trade_params):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios/{portfolio_id}/trades' page is posted to (POST) when the user is logged in
         and invalid trade params are passed
    THEN check that an error response is returned to the user
    """
    trade_params = create_random_trade_params()
    for param in invalid_trade_params.keys():
        trade_params[param] = invalid_trade_params[param]
    response = test_client.post("/api/portfolios/1/trades", json=trade_params)
    assert response.status_code == 400
    assert db.session.execute(func.count(Trade.id)).scalar() == 0


def test_successful_trade_create(test_client, create_portfolio):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios' page is posted to (POST) when the user is logged in
    THEN check that the response is successful and
         that the trade has been inserted in the database
    """
    trade_params = create_random_trade_params()
    response = test_client.post("/api/portfolios/1/trades", json=trade_params)
    assert response.status_code == 201
    trade = response.json
    # Convert from string to datetime object for comparison
    trade["trade_datetime"] = datetime.fromisoformat(trade["trade_datetime"]).replace(
        tzinfo=None
    )
    assert trade["id"] == 1
    assert trade["portfolio_id"] == 1
    trade_params["id"] = trade["id"]
    trade_params["portfolio_id"] = trade["portfolio_id"]
    trade_params["created_at"] = trade["created_at"]
    trade_params["updated_at"] = trade["updated_at"]
    assert trade == trade_params
    assert db.session.execute(func.count(Trade.id)).scalar() == 1


def test_unauthenticated_trade_update(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios/{portfolio_id}/trades/{trade_id}'
         page is put to (PUT) when the user isn't logged in
    THEN check that an error response is returned to the user
    """
    response = test_client.put(
        "/api/portfolios/1/trades/1", json=create_random_trade_params()
    )
    assert response.status_code == 401


def test_unauthorized_trade_update(test_client, login_user, create_new_user_portfolio):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios/{portfolio_id}/trades/{trade_id}' page is put to (PUT)
         when the user is logged in and the portfolio with a given id belongs to other user
    THEN check that an error response is returned to the user
    """
    response = test_client.put(
        "/api/portfolios/1/trades/1", json=create_random_trade_params()
    )
    assert response.status_code == 403


@pytest.mark.parametrize(
    "invalid_trade_params",
    [
        {
            "currency_id": -1,
        },
        {
            "currency_id": 9999,
        },
        {
            "security_id": -1,
        },
        {
            "security_id": 9999,
        },
        {
            "trade_type": "invalid trade type",
        },
        {
            "trade_datetime": "it's not a datetime",
        },
        {
            "unit_price": -9.999,
        },
        {
            "unit_price": 0,
        },
        {
            "quantity": -10,
        },
        {
            "quantity": 0,
        },
        {
            "brokerage_fee": -9.999,
        },
    ],
)
def test_invalid_trade_update(test_client, create_trade, invalid_trade_params):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios/{portfolio_id}/trades/{trade_id}'
         page is put to (PUT) when the user is logged in
         and invalid trade params are passed
    THEN check that an error response is returned to the user
    """
    trade_params = create_random_trade_params()
    for param in invalid_trade_params.keys():
        trade_params[param] = invalid_trade_params[param]
    response = test_client.put("/api/portfolios/1/trades/1", json=trade_params)
    assert response.status_code == 400


def test_successful_trade_update(test_client, create_trade):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios/{portfolio_id}/trades/{trade_id}'
         page is put to (PUT) when the user is logged in
    THEN check that the response is successful and
         that the trade has been updated in the database
    """
    new_trade_params = create_random_trade_params()
    new_trade_params["currency_id"] = 2
    new_trade_params["security_id"] = 2
    new_trade_params["trade_type"] = "sell"
    new_trade_params["unit_price"] = 100.00
    new_trade_params["quantity"] = 1.80
    new_trade_params["brokerage_fee"] = 1.15

    response = test_client.put("/api/portfolios/1/trades/1", json=new_trade_params)
    assert response.status_code == 200
    updated_trade = response.json
    # Convert from string to datetime object for comparison
    updated_trade["trade_datetime"] = datetime.fromisoformat(
        updated_trade["trade_datetime"]
    ).replace(tzinfo=None)
    assert 1 == updated_trade["id"]
    assert existing_trade["portfolio_id"] == updated_trade["portfolio_id"]
    new_trade_params["id"] = updated_trade["id"]
    new_trade_params["portfolio_id"] = updated_trade["portfolio_id"]
    new_trade_params["created_at"] = updated_trade["created_at"]
    new_trade_params["updated_at"] = updated_trade["updated_at"]
    assert updated_trade == new_trade_params


def test_unauthenticated_trade_delete(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios/{portfolio_id}/trades'
         page is requested (DELETE) when the user isn't logged in
    THEN check that an error response is returned to the user
    """
    response = test_client.delete("/api/portfolios/1/trades/1")
    assert response.status_code == 401


def test_unauthorized_trade_delete(test_client, login_user, create_new_user_portfolio):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios/{portfolio_id}/trades/{trade_id}' page is requested (DELETE)
         when the user is logged in and the portfolio with a given id belongs to other user
    THEN check that an error response is returned to the user
    """
    response = test_client.delete("/api/portfolios/1/trades/1")
    assert response.status_code == 403


def test_successful_trade_delete(test_client, create_trade):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/portfolios/{portfolio_id}/trades/{trade_id}'
         page is requested (DELETE) when the user is logged in
    THEN check that the response is successful and
         that the trade has been updated in the database
    """
    response = test_client.delete("/api/portfolios/1/trades/1")
    assert response.status_code == 200
