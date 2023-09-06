import threading


class ThreadSafeCache:
    def __init__(self):
        """
        Initialize the thread safe cache.
        """
        self._items = list()
        self._lock = threading.Lock()

    def add_item(self, item):
        """
        Adds an item to the cache.

        :param item: The item.
        """
        with self._lock:
            self._items.append(item)

    def add_items(self, items):
        """
        Adds items to the cache.

        :param items: The items.
        """
        with self._lock:
            self._items += items

    def clear(self):
        """
        Clears the cache.
        """
        with self._lock:
            self._items.clear()

    def get_all_items(self) -> list[str]:
        """
        Gets all items.
        """
        with self._lock:
            return list(self._items)
