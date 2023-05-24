from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_security import Security

# SQLALchemy must be initialized before Marshmallow
db = SQLAlchemy()

# Init Migrate
migrate = Migrate()

# Init Marshmallow
marshmallow = Marshmallow()

# Init Flask-Security
security = Security()
