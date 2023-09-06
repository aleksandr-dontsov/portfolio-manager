# The class represents the currency exchange rate
class ExchangeRate:
    def __init__(self, from_currency, to_currency, ask, bid):
        """
        Initialize the currency exchange rate.

        :param from_currency: The 'from' currency
        :param to_currency: The 'to' currency
        :param ask: The ask price
        :param bid: The bid price
        """
        self._from_currency = from_currency
        self._to_currency = to_currency
        self._ask = float(ask)
        self._bid = float(bid)

    def midpoint_rate(self):
        """
        Calculates the midpoint rate.

        :return: The midpoint rate.
        """
        return round((self._bid + self._ask) / 2, 2)

    def get_from_currency(self):
        """
        Gets the 'from' currency.

        :return: The 'from' currency.
        """
        return self._from_currency

    def get_to_currency(self):
        """
        Gets the 'to' currency.

        :return: The 'to' currency.
        """
        return self._to_currency
