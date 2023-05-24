import pathlib
from connexion import FlaskApp
from connexion.resolver import RelativeResolver
from app.extensions import db, migrate, marshmallow, security
from app.models.user import user_datastore
from app.common import make_error_response


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


def unauthn_callback(mechanisms, headers=None):
    return make_error_response(401, "Unauthorized")


def initialize_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    marshmallow.init_app(app)
    security.init_app(app, user_datastore)
    security.unauthn_handler(unauthn_callback)


def configure_logging(app):
    pass


def register_error_handlers(app):
    pass
