from app.extensions import db, market_data_api
from app.common import make_error_response, PortmanError
from app.models.portfolio import (
    Security,
    SecurityStatus,
    securities_schema,
    security_schema,
)
from flask import current_app
from flask_jwt_extended import jwt_required
from datetime import datetime, timezone

SECURITIES_UPDATE_INTERVAL_HOURS = 24
API_SECURITY_MODEL = [
    "symbol",
    "name",
    "exchange",
    "assetType",
    "ipoDate",
    "delistingDate",
    "status",
]


def validate_security_model(actual: list[str], expected: list[str]):
    if len(actual) != len(expected):
        current_app.logger.error(
            f"Cannot load securities. Unexpected security model received, {actual}"
        )
        raise PortmanError(400, "Cannot load securities")

    for actual_column, expected_column in zip(actual, expected):
        if actual_column != expected_column:
            current_app.logger.error(
                f"Cannot load securities. Unexpected security model received, {actual}"
            )
            raise PortmanError(400, "Cannot load securities")


def load_securities() -> list[Security]:
    securities = []
    try:
        rows, _ = market_data_api.get_listing_status()
        security_model = next(rows)
        validate_security_model(security_model, API_SECURITY_MODEL)
        while True:
            row = next(rows)
            securities.append(
                security_schema.load(
                    {
                        "symbol": row[0],
                        "name": row[1],
                        "exchange": row[2],
                        "asset_type": row[3].upper(),
                        "status": row[6].upper(),
                    }
                )
            )
    except StopIteration:
        pass
    current_app.logger.info(
        f"Successfully loaded {len(securities)} securities from the market data source"
    )
    return securities


def update_db_securities_list(
    api_securities: list[Security], db_securities: list[Security]
) -> list[Security]:
    update_stats = {
        "new": [],
        "delisted": [],
    }
    db_securities_dict = {security.symbol: security for security in db_securities}
    for api_security in api_securities:
        # Update an existing security
        if api_security.symbol in db_securities_dict:
            db_security = db_securities_dict[api_security.symbol]
            db_security.name = api_security.name
            db_security.exchange = api_security.exchange
            db_security.asset_type = api_security.asset_type
        else:
            # Add a new security
            db.session.add(api_security)
            update_stats["new"].append(security_schema.dump(api_security))

    # Check for delisted securities
    api_securities_set = set(security.symbol for security in api_securities)
    for db_security in db_securities_dict.values():
        if db_security.symbol not in api_securities_set:
            db_security.status = SecurityStatus.delisted
            update_stats["delisted"].append(security_schema.dump(db_security))

    db.session.commit()
    db.session.rollback()
    current_app.logger.info(f"Securities update statistics: {update_stats}")
    return securities_schema.dump(db_securities)


@jwt_required()
def read_all():
    try:
        db_securities = list(db.session.execute(db.select(Security)).scalars())
        if not db_securities:
            current_app.logger.info("Populate securities table")
            return update_db_securities_list(
                api_securities=load_securities(), db_securities=db_securities
            )

        update_datetime = db_securities[0].updated_at
        update_delta = datetime.now(timezone.utc) - update_datetime
        update_delta_hours = update_delta.total_seconds() / 3600
        if update_delta_hours > SECURITIES_UPDATE_INTERVAL_HOURS:
            current_app.logger.info("Update securities table")
            return update_db_securities_list(
                api_securities=load_securities(), db_securities=db_securities
            )

        return securities_schema.dump(db_securities), 200
    except PortmanError as error:
        return make_error_response(error.status, error.detail)
    except Exception as error:
        db.session.rollback()
        return make_error_response(500, f"Cannot get security entries, error: {error}")
