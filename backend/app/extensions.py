from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

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
