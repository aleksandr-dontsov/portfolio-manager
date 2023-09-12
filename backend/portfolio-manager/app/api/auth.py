from app.components.extensions import db, bcrypt
from app.components.errors import make_error_response
from app.components.config import Config
from app.models.user import User
from email_validator import validate_email, EmailNotValidError
from password_strength import PasswordPolicy
from flask import jsonify
from flask_jwt_extended import (
    create_access_token,
    get_current_user,
    jwt_required,
    set_access_cookies,
)


def make_success_response(id: int, email: str, message: str):
    return jsonify({"id": id, "email": email, "message": message})


def get_user_by_email(email: str):
    return db.session.execute(db.select(User).filter_by(email=email)).scalar()


def validate_password(password: str):
    password_policy = PasswordPolicy.from_names(
        length=Config.MIN_PASSWORD_LENGTH, uppercase=1, special=1
    )
    result = password_policy.test(password)
    if result:
        raise ValueError(result)


def signup(credentials):
    try:
        # Ensure a user doesn't exist
        email = credentials["email"]
        existing_user = get_user_by_email(email)
        if existing_user is not None:
            return make_error_response(
                400, f"User with email {credentials['email']} already exists"
            )
        # Validate email
        try:
            email = validate_email(email).normalized
        except EmailNotValidError as error:
            return make_error_response(400, f"{error}")
        # Validate password
        password = credentials["password"]
        try:
            validate_password(password)
        except Exception as error:
            return make_error_response(400, f"{error}")
        # Save a user to db
        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = User(email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return make_success_response(
            new_user.id, new_user.email, "User successfully signed up"
        )
    except Exception as error:
        return make_error_response(500, f"{error}")


def login(credentials):
    try:
        # Validate email
        email = credentials["email"]
        try:
            email = validate_email(email).normalized
        except EmailNotValidError as error:
            return make_error_response(400, f"{error}")
        # Get a user
        user = get_user_by_email(email)
        if user is None:
            return make_error_response(404, f"User with email {email} not found")
        # Check a password against a given salted and hashed password value
        if not user.check_password(credentials["password"]):
            return make_error_response(400, f"Wrong password for {email}")
        # Create a JWT
        access_token = create_access_token(identity=user)
        response = make_success_response(
            user.id, user.email, "User successfully logged in"
        )
        set_access_cookies(response=response, encoded_access_token=access_token)
        return response
    except Exception as error:
        return make_error_response(500, f"{error}")


@jwt_required()
def change_password(passwords):
    try:
        current_user = get_current_user()
        # Verify a current password
        current_password = passwords["current_password"]
        if not current_user.check_password(current_password):
            return make_error_response(400, f"Wrong password for {current_user.email}")
        new_password = passwords["new_password"]
        # Check if new password equals to the current one
        if new_password == current_password:
            return make_error_response(
                400, "New password cannot be the same as old password"
            )
        # Validate a new password
        try:
            validate_password(new_password)
        except Exception as error:
            return make_error_response(400, f"{error}")
        # Set a new password
        new_password_hash = bcrypt.generate_password_hash(new_password).decode("utf-8")
        current_user.password_hash = new_password_hash
        db.session.commit()
        return make_success_response(
            current_user.id,
            current_user.email,
            "User successfully changed the password",
        )
    except Exception as error:
        return make_error_response(500, f"{error}")
