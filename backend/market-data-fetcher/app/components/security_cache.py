from app.components.security import Security
import threading


class SecurityCache:
    def __init__(self):
        """
        Initialize the security cache.
        """
        self._securities = dict()
        self._lock = threading.Lock()

    def has_security(self, symbol: str) -> bool:
        """
        Checks if a security is in the cache in a thread-safe manner.

        :param symbol: The security symbol.
        :return: True if the security with a symbol is in the cache, False if it doesn't exist.
        """
        with self._lock:
            return symbol in self._securities

    def update_security(self, symbol: str, security: Security):
        """
        Update a security in the cache in a thread-safe manner.

        :param symbol: The security symbol.
        :param security: The security info.
        """
        with self._lock:
            self._securities[symbol] = security

    def remove_security(self, symbol: str) -> bool:
        """
        Remove a security from the cache in a thread-safe manner.

        :param symbol: The security symbol.
        :return: True if the symbol was removed, False if it didn't exist.
        """
        with self._lock:
            if not self.has_security(symbol):
                return False

            self._securities.remove(symbol)

    def get_security(self, symbol: str) -> Security:
        """
        Get a security managed by the cache in a thread-safe manner.

        :param symbol: The security symbol.
        :return: The security.
        """
        with self._lock:
            return self._securities[symbol]

    def get_securities(self, symbols: list[str]) -> list[Security]:
        """
        Get a list of securities managed by the cache in a thread-safe manner.

        :param symbol: The security symbols.
        :return: The security list.
        """
        with self._lock:
            return [self._securities[symbol] for symbol in symbols]

    def get_all_securities(self) -> list[Security]:
        """
        Get all securities managed by the cache in a thread-safe manner.

        :return: The security list.
        """
        with self._lock:
            return self._securities.values()
