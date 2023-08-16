from app.extensions import db, bcrypt, jwt


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True, server_default="")
    email_confirmed_at = db.Column(db.DateTime(), nullable=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(120), nullable=False, server_default="")
    second_name = db.Column(db.String(120), nullable=False, server_default="")
    created_at = db.Column(db.DateTime(), default=db.func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime(), default=db.func.now(), nullable=False, onupdate=db.func.now()
    )
    is_active = db.Column(db.Boolean(), nullable=False, server_default="1")

    portfolios = db.relationship(
        # back_populates - establishes a bidirectional relationship allowing to access a user
        #                  holding a given portfolio
        # delete-orphan - removes a portfolio object when a user associated with it is deleted or
        #                 when a portfolio object is not associated with any user
        "Portfolio",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<User {self.email}>"

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(pw_hash=self.password_hash, password=password)


# Register a callback that converts and identity to json a JSON serializable format
# when creating JWTs
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


# Register a callback that loads a user from db whenever a protected route is accessed.
# The callback should return an object on successful lookup, or None if the lookup failed
# for any reason (e.g. the user has been deleted from db)
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    id = jwt_data["sub"]
    return db.session.execute(db.select(User).filter_by(id=id)).scalar()
