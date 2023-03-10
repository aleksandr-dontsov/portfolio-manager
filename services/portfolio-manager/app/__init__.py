import pathlib
from connexion import FlaskApp
from connexion.resolver import RelativeResolver
from app.extensions import db, ma, se
from app.models.user import user_datastore


def create_app(config_name):
    # Flask app is created internally
    basedir = pathlib.Path(__file__).parent.resolve()
    connexion_app = FlaskApp(__name__, specification_dir=basedir.parent)
    connexion_app.add_api("swagger.yml", resolver=RelativeResolver("app.views"))

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
    from app.manage import bp as bp_db

    app.register_blueprint(bp_db)


def initialize_extensions(app):
    db.init_app(app)
    ma.init_app(app)
    se.init_app(app, user_datastore)


def configure_logging(app):
    pass


def register_error_handlers(app):
    pass
