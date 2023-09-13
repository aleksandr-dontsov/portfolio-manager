from app.components.extensions import db
from app.components.market_data_fetcher import market_data_fetcher
from app.models.portfolio import (
    Security,
    AssetType,
    SecurityStatus,
    security_schema,
)
from flask import current_app
from datetime import datetime, timezone


class SecuritiesManager:
    def __init__(self):
        pass

    def init_app(self, app):
        self._update_interval_hours = app.config.get("SECURITIES_UPDATE_INTERVAL_HOURS")
        self._max_search_number = app.config.get("SECURITIES_MAX_SEARCH_RESULTS")
        with app.app_context():
            self._securities = db.session.execute(db.select(Security)).scalars().all()

    def search_securities(self, query: str) -> list[Security]:
        if not query:
            return []
        query = query.lower()

        def is_match(security):
            if security.status == SecurityStatus.delisted:
                return False
            return query in security.symbol.lower() or query in security.name.lower()

        matched_securities = list(filter(is_match, self._securities))
        return matched_securities[: self._max_search_number]

    def update_securities(self, new_securities: list[Security]):
        try:
            update_stats = {
                "new": [],
                "delisted": [],
            }
            securities_dict = {
                security.symbol: security for security in self._securities
            }
            for new_security in new_securities:
                # Update an existing security
                if new_security.symbol in securities_dict:
                    security = securities_dict[new_security.symbol]
                    security.name = new_security.name
                    security.exchange = new_security.exchange
                    security.asset_type = new_security.asset_type
                else:
                    # Add a new security
                    db.session.add(new_security)
                    self._securities.append(new_security)
                    update_stats["new"].append(security_schema.dump(new_security))

            # Check for delisted securities
            new_securities_set = set(security.symbol for security in new_securities)
            for security in securities_dict.values():
                if security.symbol not in new_securities_set:
                    security.status = SecurityStatus.delisted
                    update_stats["delisted"].append(security_schema.dump(security))

            db.session.commit()
            current_app.logger.info("Successfully updated securities.")
        except Exception as error:
            db.session.rollback()
            current_app.logger.error(f"Unable to update securities. {error}")
            raise error

    def load_securities(self) -> list[Security]:
        securities = []
        for security in market_data_fetcher.get_traded_securities():
            if security["assetType"] not in AssetType._member_map_:
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

    def is_update_required(self):
        if not self._securities:
            return True
        last_update_datetime_utc = self._securities[0].updated_at
        update_delta = datetime.now(timezone.utc) - last_update_datetime_utc
        update_delta_hours = update_delta.total_seconds() / 3600
        return update_delta_hours > self._update_interval_hours


securities_manager = SecuritiesManager()
