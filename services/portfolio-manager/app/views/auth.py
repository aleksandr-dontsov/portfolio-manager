from flask import make_response, abort
from flask_security import (
    hash_password,
    verify_password,
    login_user,
    logout_user,
    auth_required,
    current_user
)
from app.extensions import se

def signup(credentials):
    existing_user = se.datastore.find_user(email=credentials['email'])
    if existing_user is not None:
        abort(406, f"User with email {credentials['email']} already exists")
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

@auth_required()
def logout():
    email = current_user.email
    logout_user()
    return make_response(
        f"User {email} logged out", 200)

@auth_required()
def change_password(passwords):
    if not verify_password(password=passwords['current_password'], password_hash=current_user.password):
        abort(400, f"Wrong password for {current_user.email}")

    current_user.password = hash_password(passwords['new_password'])
    se.datastore.db.session.merge(current_user)
    se.datastore.db.session.commit()
    return make_response(
        f"Password for {current_user.email} has been successfully changed ", 200)