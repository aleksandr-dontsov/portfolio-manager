from app.components.application import application
from connexion import FlaskApp
from connexion.resolver import RelativeResolver
import pathlib
import os


def create_app(config_name):
    # Create a Flask app with an OpenAPI specification
    basedir = pathlib.Path(__file__).parent.resolve()
    connexion_app = FlaskApp(__name__, specification_dir=basedir.parent)
    connexion_app.add_api("swagger.yml", resolver=RelativeResolver("app.api"))

    # Configure underlying Flask app
    app = connexion_app.app
    config_module = f"app.components.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)

    def is_debug_mode():
        """Get app debug status."""
        debug = os.environ.get("FLASK_DEBUG")
        if not debug:
            return os.environ.get("FLASK_ENV") == "development"
        return debug.lower() not in ("0", "false", "no")

    def is_werkzeug_reloader_process():
        """Get werkzeug status."""
        return os.environ.get("WERKZEUG_RUN_MAIN") == "true"

    # Avoid starting scheduler two times when the developement server is used
    if is_debug_mode() and not is_werkzeug_reloader_process():
        return app

    application.init_app(app)

    return app
