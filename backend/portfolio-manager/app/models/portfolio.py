import enum

from app.extensions import db, marshmallow

from marshmallow_enum import EnumField
from marshmallow_sqlalchemy import fields


class Currency(db.Model):
    __tablename__ = "currency"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.CHAR(3), nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)

    portfolios = db.relationship(
        "Portfolio",
        back_populates="currency",
        cascade="all, delete",
        passive_deletes=True,
    )
    trades = db.relationship(
        "Trade",
        back_populates="currency",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Portfolio(db.Model):
    __tablename__ = "portfolio"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey("currency.id"), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=db.func.now()
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=db.func.now(),
        onupdate=db.func.now(),
    )

    user = db.relationship("User", back_populates="portfolios")
    currency = db.relationship("Currency", back_populates="portfolios")
    # Provides a relationship between two mapped classes
    trades = db.relationship(
        "Trade",
        back_populates="portfolio",
        cascade="all, delete-orphan",
        order_by="desc(Trade.trade_datetime)",
    )


class AssetType(enum.Enum):
    stock = "STOCK"
    etf = "ETF"


class Security(db.Model):
    __tablename__ = "security"

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(5), nullable=False)
    name = db.Column(db.String, nullable=False)
    exchange = db.Column(db.String, nullable=False)
    asset_type = db.Column(db.Enum(AssetType), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False, server_default="1")

    trades = db.relationship(
        "Trade", back_populates="security", cascade="all, delete-orphan"
    )


class TradeType(enum.Enum):
    buy = "BUY"
    sell = "SELL"


class Trade(db.Model):
    __tablename__ = "trade"

    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey("portfolio.id"), nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey("currency.id"), nullable=False)
    security_id = db.Column(db.Integer, db.ForeignKey("security.id"), nullable=False)
    trade_type = db.Column(db.Enum(TradeType), nullable=False)
    trade_datetime = db.Column(db.DateTime(timezone=True), nullable=False)
    unit_price = db.Column(
        db.Float(precision=2),
        db.CheckConstraint(sqltext="unit_price > 0", name="valid_unit_price"),
        nullable=False,
    )
    quantity = db.Column(
        db.Float(precision=2),
        db.CheckConstraint(sqltext="quantity > 0", name="valid_quantity"),
        nullable=False,
    )
    brokerage_fee = db.Column(
        db.Float(precision=2),
        db.CheckConstraint(sqltext="brokerage_fee >= 0", name="valid_brokerage_fee"),
        nullable=False,
    )
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=db.func.now()
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=db.func.now(),
        onupdate=db.func.now(),
    )

    portfolio = db.relationship("Portfolio", back_populates="trades")
    currency = db.relationship("Currency", back_populates="trades")
    security = db.relationship("Security", back_populates="trades")


class SecuritySchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Security
        load_instance = True
        include_fk = False
        include_relationships = False

    asset_type = EnumField(AssetType, by_value=True)


class CurrencySchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Currency
        load_instance = True
        include_fk = False


class TradeSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Trade
        load_instance = True
        include_fk = True
        include_relationships = True

    trade_type = EnumField(TradeType, by_value=True)
    security = fields.Nested(SecuritySchema, many=False)


trade_schema = TradeSchema()
trades_schema = TradeSchema(many=True)


# Inherit from marshmallow.SQLAlchemyAutoSchema
# to find a SQLAlchemy model and a SQLAlchemy session
class PortfolioSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        # This is how Marshmallow finds attributes in the Portfolio
        # class and learns the types of those attributes
        model = Portfolio
        # Here we enable deserialization of JSON data and
        # load of Portfolio model instances from it
        load_instance = True
        # Support foreign keys
        include_fk = True
        # Add related objects to the schema
        include_relationships = True

    trades = fields.Nested(TradeSchema, many=True)
    currency = fields.Nested(CurrencySchema, many=False)


portfolio_schema = PortfolioSchema()
portfolios_schema = PortfolioSchema(many=True)
