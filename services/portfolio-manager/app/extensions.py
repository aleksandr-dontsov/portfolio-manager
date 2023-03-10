from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_security import Security

# SQLALchemy must be initialized before Marshmallow
db = SQLAlchemy()

# Init Marshmallow
ma = Marshmallow()

# Init Flask-Security
se = Security()
