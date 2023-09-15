from app.components.extensions import db
from app.models.portfolio import (
    Security,
    SecurityStatus,
)
from flask import current_app


class SecuritiesManager:
    def __init__(self):
        pass

    def init_app(self, app):
        self._max_search_number = app.config.get("SECURITIES_MAX_SEARCH_RESULTS")

    def search_securities(self, query: str) -> list[Security]:
        try:
            if not query:
                return []
            query = query.lower()

            def is_match(security):
                if security.status == SecurityStatus.delisted:
                    return False
                return (
                    query in security.symbol.lower() or query in security.name.lower()
                )

            # TODO: add caching
            securities = db.session.scalars(db.select(Security)).all()
            matched_securities = list(filter(is_match, securities))
            return matched_securities[: self._max_search_number]
        except Exception as error:
            current_app.logger.info(error)


securities_manager = SecuritiesManager()
