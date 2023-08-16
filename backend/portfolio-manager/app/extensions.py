from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from alpha_vantage.alphavantage import AlphaVantage as av
from datetime import date


# Market Data API
class MarketDataApi(av):
    def __init__(self):
        pass

    def init_app(self, app):
        super(MarketDataApi, self).__init__(
            key=app.config.get("ALPHA_VANTAGE_API_KEY"), output_format="csv"
        )

    # def get_listing_status(self, date = date.today(), status = 'active'):
    @av._output_format
    @av._call_api_on_func
    def get_listing_status(self, date=date.today(), state="active"):
        _FUNCTION_KEY = "LISTING_STATUS"
        return _FUNCTION_KEY, "date", "state"


# SQLALchemy must be initialized before Marshmallow
db = SQLAlchemy()

# Init Migrate
migrate = Migrate()

# Init Marshmallow
marshmallow = Marshmallow()

# Init JWT Manager
jwt = JWTManager()

# Init Bcrypt
bcrypt = Bcrypt()

# Init Market Data API
market_data_api = MarketDataApi()
