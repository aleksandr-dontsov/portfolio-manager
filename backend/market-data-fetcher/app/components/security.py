# The class represents the security
class Security:
    def __init__(
        self, symbol: str, name: str, price: int, exchange: str, assetType: str
    ):
        """
        Initialize the security instance.

        :param symbol: The security symbol
        :param name: The security name
        :param price: The latest market price
        :param exchange: The exchange short name
        :param assetType: The asset type of the security
        """
        self._symbol = symbol
        self._name = name
        self._price = price
        self._exchange = exchange
        self._assetType = assetType

    def get_symbol(self):
        """
        Gets the security symbol.

        :return: The security symbol.
        """
        return self._symbol

    def get_name(self):
        """
        Gets the security name.

        :return: The security name.
        """
        return self._name

    def get_price(self):
        """
        Gets the security price.

        :return: The security price.
        """
        return self._price

    def get_exchange(self):
        """
        Gets the security exchange.

        :return: The security exchange.
        """
        return self._exchange

    def get_asset_type(self):
        """
        Gets the asset type.

        :return: The security asset type.
        """
        return self._assetType

    def to_dict(self):
        """
        Returns a dictionary representation of the object.

        :return: The dictionary representation of the object.
        """
        return {
            "symbol": self._symbol,
            "name": self._name,
            "price": self._price,
            "exchange": self._exchange,
            "assetType": self._assetType,
        }


def get_quotes(securities: list[Security]):
    return {security.get_symbol(): security.get_price() for security in securities}
