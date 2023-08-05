from app.extensions import db, migrate, marshmallow, jwt, bcrypt
from connexion import FlaskApp
from connexion.resolver import RelativeResolver
from flask_jwt_extended import (
    get_jwt,
    create_access_token,
    set_access_cookies,
    get_current_user,
)
import pathlib
from datetime import datetime, timezone, timedelta


def create_app(config_name):
    # Flask app is created internally
    basedir = pathlib.Path(__file__).parent.resolve()
    connexion_app = FlaskApp(__name__, specification_dir=basedir.parent)
    connexion_app.add_api("swagger.yml", resolver=RelativeResolver("app.api"))

    # Configure underlying Flask app
    app = connexion_app.app
    config_module = f"app.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)

    register_blueprints(app)

    initialize_extensions(app)

    configure_logging(app)

    register_error_handlers(app)

    return app


def register_blueprints(app):
    pass


def initialize_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    marshmallow.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Refresh token that will expire in less than 30 minutes
    @app.after_request
    def refresh_expiring_jws(response):
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            tartget_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            # TODO: Check how refreshing of the token works
            if tartget_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_current_user())
                set_access_cookies(response, access_token)
            return response
        except (RuntimeError, KeyError):
            # There is not a valid JWT
            return response


def configure_logging(app):
    pass


def register_error_handlers(app):
    pass
