from flask import current_app
from app.components.security import get_quotes
from app.components.application import application


def quote(securities: list[str]):
    try:
        current_app.logger.info(f"Subscribe for {securities} security quotes")
        cached_securities = application.get_securities()
        result = []
        for security in securities:
            # Add a symbol to the cache of symbols for quote updates
            symbols = application.get_symbols()
            symbols.add_item(security)

            if cached_securities.has_security(security):
                result.append(cached_securities.get_security(security))
            else:
                current_app.logger.info(
                    f"Security '{security}' hasn't been found in the cache"
                )

        # Return cached quotes to the client
        return get_quotes(result), 200
    except Exception as error:
        return {"message": str(error)}, 500


def fx(currencies: list[str]):
    try:
        current_app.logger.info(f"Get {currencies} exchange rates")
        exchange_rates = []
        for rate in application.get_exchange_rates().get_all_items():
            from_currency = rate.get_from_currency()
            to_currency = rate.get_to_currency()
            if from_currency != "USD":
                continue
            if to_currency not in currencies:
                continue
            exchange_rates.append(
                {
                    "from": from_currency,
                    "to": to_currency,
                    "rate": rate.midpoint_rate(),
                }
            )
        return exchange_rates, 200
    except Exception as error:
        return {"message": str(error)}, 500


def security():
    try:
        current_app.logger.info("Get the traded security list")
        securities = application.get_securities().get_all_securities()
        return [security.to_dict() for security in securities], 200
    except Exception as error:
        return {"message": str(error)}, 500
