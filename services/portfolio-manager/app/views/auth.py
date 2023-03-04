import re
import json
from flask import make_response, abort, current_app
from flask_security import (
    hash_password,
    verify_password,
    login_user,
    logout_user,
    auth_required,
    permissions_required,
    current_user
)
from app.extensions import se

def check_password(password, password_length):
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        password_length characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """

    # Calculating length
    length_error = len(password) < password_length

    # Searching for digits
    digit_error = re.search(r"\d", password) is None

    # Searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # Searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # Searching for symbols
    symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', password) is None

    # Overall result
    password_ok = not (
        length_error or digit_error or uppercase_error or lowercase_error or symbol_error)

    return {
        "password_ok": password_ok,
        "length_error": length_error,
        "digit_error": digit_error,
        "uppercase_error": uppercase_error,
        "lowercase_error": lowercase_error,
        "symbol_error": symbol_error
    }

def signup(credentials):
    if not credentials['email']:
        abort(400, "Email cannot be empty")

    existing_user = se.datastore.find_user(email=credentials['email'])
    if existing_user is not None:
        abort(406, f"User with email {credentials['email']} already exists")

    criterias = check_password(
        credentials['password'],
        # current_app is a proxy to the application hadnling this request
        # flask automatically pushes an application context when handling a request
        current_app.config['SECURITY_PASSWORD_LENGTH_MIN'])
    if not criterias['password_ok']:
        abort(400, json.dumps(criterias))

    se.datastore.create_user(
        email=credentials['email'], password=hash_password(credentials['password']), roles=["user"])
    se.datastore.db.session.commit()
    return make_response(
        f"User {credentials['email']} successfully signed up", 201)

def login(credentials):
    existing_user = se.datastore.find_user(email=credentials['email'])
    if existing_user is None:
        abort(400, f"User with email {credentials['email']} not found")

    # Check a password against a given salted and hashed password value
    if not verify_password(password=credentials['password'], password_hash=existing_user.password):
        abort(400, f"Wrong password for {credentials['email']}")

    # Remember flag prevents a user from being logged out
    # when the browser is closed
    if not login_user(user=existing_user, remember=True):
        abort(400)

    # TODO validate value of the next parameter, otherwise
    # application will be vulnerable to open redirects
    # https://web.archive.org/web/20120517003641/http://flask.pocoo.org/snippets/62/

    return make_response(
        f"User {credentials['email']} logged in", 200)

@auth_required("session")
@permissions_required("user-read")
def logout():
    email = current_user.email
    logout_user()
    return make_response(
        f"User {email} logged out", 200)

@auth_required("session")
@permissions_required("user-read")
def change_password(passwords):
    if not verify_password(password=passwords['current_password'], password_hash=current_user.password):
        abort(400, f"Wrong password for {current_user.email}")

    criterias = check_password(
        passwords['new_password'],
        current_app.config['SECURITY_PASSWORD_LENGTH_MIN'])
    if not criterias['password_ok']:
        abort(400, json.dumps(criterias))

    current_user.password = hash_password(passwords['new_password'])
    se.datastore.db.session.merge(current_user)
    se.datastore.db.session.commit()
    return make_response(
        f"Password for {current_user.email} has been successfully changed ", 200)