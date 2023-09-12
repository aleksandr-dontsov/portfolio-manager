"""
This file (test_auth.py) contains the functional tests for the auth views.

These tests use GET and POST methods to different URLs to check for the proper
behavior of the auth views.
"""

import pytest
from conftest import registered_user, new_user
from flask_security import current_user
from app.components.extensions import security


def test_signup_form(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/signup' page is requested (GET)
    THEN check that the processing of the request is not allowed
    """
    response = test_client.get("/api/signup")
    assert response.status_code == 405


def test_successful_signup(init_database, test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/signup' page is posted to (POST)
    THEN check that the response is successful, the user is in the database,
         and that the user is not logged it
    """
    response = test_client.post("/api/signup", json=new_user)
    assert response.status_code == 201
    user = security.datastore.find_user(email=new_user["email"])
    assert user.email == new_user["email"]
    assert user.password == new_user["password"]


@pytest.mark.parametrize(
    "email",
    [None, "", "no@domain", "domain.only", "@left.empty", "right.empty@"],
)
def test_invalid_email_signup(init_database, test_client, email):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/signup' page is posted to with invalid email (POST)
    THEN check that an error response is returned to the user
    """
    response = test_client.post(
        "/api/signup", json=dict(email=email, password=registered_user["password"])
    )
    assert response.status_code == 400
    assert security.datastore.find_user(email=email) is None


@pytest.mark.parametrize(
    "password",
    [None, "", "short"],
)
def test_invalid_password_signup(init_database, test_client, password):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/signup' page is posted to with invalid password (POST)
    THEN check that an error response is returned to the user
    """
    response = test_client.post(
        "/api/signup", json=dict(email=registered_user["email"], password=password)
    )
    assert response.status_code == 400
    assert security.datastore.find_user(email=registered_user["email"]) is None


def test_duplicate_signup(register_user, test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/signup' page is posted to (POST) using email address already registered
    THEN check that an error response is returned to the user
    """
    response = test_client.post("/api/signup", json=registered_user)
    assert response.status_code == 406
    assert security.datastore.find_user(email=registered_user["email"])


def test_unauthenticated_logout(init_database, test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/logout' page is posted to (POST) when the user isn't logged in
    THEN check that an error response is returned to the user
    """
    response = test_client.post("/api/logout")
    assert response.status_code == 401


def test_successful_login(register_user, test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to (POST) using valid credentials
    THEN check that the response is successful and the user is logged in
    """
    response = test_client.post("/api/login", json=registered_user)
    assert response.status_code == 200
    assert current_user.email == registered_user["email"]
    assert current_user.is_authenticated

    response = test_client.post("/api/logout")
    assert response.status_code == 200
    assert not current_user.is_authenticated


def test_invalid_email_login(init_database, test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to (POST) using invalid email
    THEN check that an error response is returned to the user
    """
    response = test_client.post(
        "/api/login", json={"email": "", "password": registered_user["password"]}
    )
    assert response.status_code == 400


def test_invalid_password_login(init_database, test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to (POST) using invalid email
    THEN check that an error response is returned to the user
    """
    response = test_client.post(
        "/api/login", json={"email": registered_user["email"], "password": ""}
    )
    assert response.status_code == 400


def test_already_logged_in_login(test_client, login_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to (POST) when the user is already logged in
    THEN check that the response is successful and the user is logged in
    """
    response = test_client.post("/api/login", json=registered_user)
    assert response.status_code == 200
    response = test_client.post("/api/logout")
    assert response.status_code == 200


def test_unauthenticated_change_password(init_database, test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/change_password' page is posted to (POST) when the user isn't logged in
    THEN check that an error response is returned to the user
    """
    response = test_client.post(
        "/api/change_password", json={"current_password": "", "new_password": ""}
    )
    assert response.status_code == 401


def test_successfull_change_password(test_client, login_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/change_password' page is posted to (POST) when the user is already logged in
    THEN check that the response is successful and the user is logged in
    """
    response = test_client.post(
        "/api/change_password",
        json={
            "current_password": registered_user["password"],
            "new_password": new_user["password"],
        },
    )
    assert response.status_code == 200

    user = security.datastore.find_user(email=registered_user["email"])
    assert user.password == new_user["password"]
