from flask import Flask
from app.market_data_api import mda


def create_app(config_name):
    app = Flask(__name__)
    config_module = f"app.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)
    mda.init_app(app)

    @app.cli.command("load-securities")
    def load_securities():
        listing, _ = mda.get_listing_status()
        for row in listing:
            print(row)

    return app
