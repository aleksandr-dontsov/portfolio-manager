from app.extensions import db

from flask_security.models import fsqla_v3 as fsqla
from flask_security import SQLAlchemyUserDatastore

fsqla.FsModels.set_db_info(db)


# FsUserMixin provides role properties
class Role(db.Model, fsqla.FsRoleMixin):
    __tablename__ = "role"
    pass


# FsUserMixin provides user properties
class User(db.Model, fsqla.FsUserMixin):
    __tablename__ = "user"

    portfolios = db.relationship(
        "Portfolio", back_populates="user", cascade="all, delete-orphan"
    )


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
