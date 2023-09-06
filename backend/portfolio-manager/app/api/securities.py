from app.components.extensions import db
from app.components.market_data_fetcher import market_data_fetcher
from app.components.errors import make_error_response, PortfolioManagerError
from app.models.portfolio import (
    Security,
    SecurityStatus,
    AssetType,
    securities_schema,
    security_schema,
)
from flask import current_app
from flask_jwt_extended import jwt_required
from datetime import datetime, timezone


def load_securities() -> list[Security]:
    securities = []
    for security in market_data_fetcher.get_traded_securities():
        if security["assetType"] not in AssetType._member_map_:
            current_app.logger.info(security)
            continue

        securities.append(
            security_schema.load(
                {
                    "symbol": security["symbol"],
                    "name": security["name"],
                    "exchange": security["exchange"],
                    "asset_type": security["assetType"].upper(),
                    "status": SecurityStatus.active,
                }
            )
        )
    current_app.logger.info(f"Successfully loaded {len(securities)} securities")
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
    current_app.logger.info("Successfully updated securities in the database.")


@jwt_required()
def read_all():
    try:
        db_securities = db.session.execute(db.select(Security)).scalars().all()
        if not db_securities:
            current_app.logger.info("Populate securities table")
            return update_db_securities_list(
                api_securities=load_securities(), db_securities=db_securities
            )

        update_datetime = db_securities[0].updated_at
        update_delta = datetime.now(timezone.utc) - update_datetime
        update_delta_hours = update_delta.total_seconds() / 3600
        update_interval_hours = current_app.config.get(
            "SECURITIES_UPDATE_INTERVAL_HOURS"
        )
        if update_delta_hours > update_interval_hours:
            current_app.logger.info("Update securities table")
            return update_db_securities_list(
                api_securities=load_securities(), db_securities=db_securities
            )

        current_app.logger.info("No security updates")
        return securities_schema.dump(db_securities), 200
    except PortfolioManagerError as error:
        db.session.rollback()
        return make_error_response(error.status, error.detail)
    except Exception as error:
        db.session.rollback()
        return make_error_response(500, f"Cannot get security entries, error: {error}")
