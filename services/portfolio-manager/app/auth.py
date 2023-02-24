from flask import make_response, abort
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import db, login_manager
from models import User

# This callback is used to reload a user object
# from the user id stored in the session
@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(
        db.Select(User).filter_by(id=int(user_id))).scalar()

def signup(credentials):
    existing_user = db.session.execute(
        db.select(User).filter(User.email == credentials['email'])).scalar()
    if existing_user:
        abort(406, f"User with email {credentials['email']} already exists")

    new_user = User(
        email=credentials['email'],
        # Hash a password with the given method and a salt of a specified length
        password_hash=generate_password_hash(credentials['password'], method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    return make_response(
        f"User {new_user.email} successfully signed up", 201)

def login(credentials):
    existing_user = db.session.execute(
        db.select(User).filter(User.email == credentials['email'])).scalar()

    if existing_user is None:
        abort(400, f"User with email {credentials['email']} not found")

    # Check a password against a given salted and hashed password value
    if not check_password_hash(existing_user.password_hash, credentials['password']):
        abort(400, f"Wrong password for {credentials['email']}")

    if not login_user(user=existing_user, remember=True):
        abort(400)

    # TODO validate value of the next parameter, otherwise
    # application will be vulnerable to open redirects
    # https://web.archive.org/web/20120517003641/http://flask.pocoo.org/snippets/62/

    return make_response(
        f"User {credentials['email']} logged in")

@login_required
def logout():
    logout_user()
    return "Logout", 200