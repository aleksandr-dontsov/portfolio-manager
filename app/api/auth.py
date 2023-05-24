from flask_security import (
    hash_password,
    verify_password,
    login_user,
    logout_user,
    auth_required,
    permissions_required,
    current_user,
)
from app.extensions import security
from app.common import make_error_response
from email_validator import EmailNotValidError


def make_success_response(id: int, email: str, message: str, status=200):
    return {"id": id, "email": email, "message": message}, status


def signup(credentials):
    try:
        email = credentials["email"]
        existing_user = security.datastore.find_user(email=email)
        if existing_user is not None:
            return make_error_response(
                400, f"User with email {credentials['email']} already exists"
            )
        # Validate email
        try:
            email = security._mail_util.normalize(email)
        except EmailNotValidError as error:
            return make_error_response(400, f"{error}")
        # Validate password
        errors, password = security._password_util.validate(
            credentials["password"], True
        )
        if errors is not None:
            error = ".".join(errors)
            return make_error_response(400, f"{error}")
        # Save user to db
        user = security.datastore.create_user(
            email=email, password=hash_password(password), roles=["user"]
        )
        security.datastore.db.session.commit()
        return make_success_response(user.id, user.email, "User successfully signed up")
    except Exception as error:
        return make_error_response(500, f"{error}")


def login(credentials):
    try:
        user = security.datastore.find_user(email=credentials["email"])
        if user is None:
            return make_error_response(
                404, f"User with email {credentials['email']} not found"
            )
        # Check a password against a given salted and hashed password value
        if not verify_password(
            password=credentials["password"], password_hash=user.password
        ):
            return make_error_response(
                400, f"Wrong password for {credentials['email']}"
            )
        # Remember flag prevents a user from being logged out
        # when the browser is closed
        if not login_user(user=user, remember=True):
            return make_error_response(
                400, f"Unable to login a user with email {credentials['email']}"
            )
        # TODO validate value of the next parameter, otherwise
        # application will be vulnerable to open redirects
        # https://web.archive.org/web/20120517003641/http://flask.pocoo.org/snippets/62/
        return make_success_response(user.id, user.email, "User successfully logged in")
    except Exception as error:
        return make_error_response(500, f"{error}")


@auth_required("session")
@permissions_required("user-read")
def logout():
    try:
        id = current_user.id
        email = current_user.email
        logout_user()
        return make_success_response(id, email, "User successfully logged out")
    except Exception as error:
        return make_error_response(500, f"{error}")


@auth_required("session")
@permissions_required("user-read")
def change_password(passwords):
    try:
        # Verify a current password
        if not verify_password(
            password=passwords["current_password"], password_hash=current_user.password
        ):
            return make_error_response(400, f"Wrong password for {current_user.email}")
        # Validate a new password
        errors, password = security._password_util.validate(
            passwords["new_password"], True
        )
        if errors is not None:
            error = ".".join(errors)
            return make_error_response(400, f"{error}")
        current_user.password = hash_password(password)
        security.datastore.db.session.merge(current_user)
        security.datastore.db.session.commit()
        return make_success_response(
            current_user.id,
            current_user.email,
            "User successfully changed the password",
        )
    except Exception as error:
        return make_error_response(500, f"{error}")
