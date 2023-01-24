from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), nullable=False, unique=True)
    password_hash=db.Column(db.String(70), nullable=False, unique=True)
    registered_at=db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())
    updated_at=db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())

    portfolios = db.relationship(
        "Portfolio", back_populates="user", cascade="all, delete", passive_deletes=True)

    def __repr__(self):
        return f'<User {self.email}>'

class Currency(db.Model):
    __tablename__ = "currency"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.CHAR(3), nullable=False)
    name = db.Column(db.String, nullable=False)

    portfolios = db.relationship(
        "Portfolio", back_populates="currency", cascade="all, delete", passive_deletes=True)

    def __repr__(self):
        return f'<Currency {self.code}, {self.name}>'

class Portfolio(db.Model):
    __tablename__ = "portfolio"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey("currency.id"), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.now())

    currency = db.relationship("Currency", back_populates="portfolios")
    user = db.relationship("User", back_populates="portfolios")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f'<Portfolio {self.name}, {self.user_id}, {self.currency_id}>'