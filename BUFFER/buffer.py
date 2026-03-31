# filename: buffer.py

import threading
from queue import Queue, Empty


class Buffer:
    """Thread-safe data buffer.

    This class provides a real-time safe buffer that always keeps
    the most recent item. It prevents buildup of stale data in
    multi-threaded pipelines.
    """

    def __init__(self, maxsize=1):
        """Initialize buffer.

        Creates a queue with limited size to ensure that only the
        most recent item is stored. This is critical for real-time
        systems such as video pipelines.
        """
        self.queue = Queue(maxsize=maxsize)
        self.lock = threading.Lock()

    def put(self, item):
        """Insert item into buffer.

        Adds new data to the buffer. If the buffer is full,
        the oldest item is removed to maintain real-time behavior.
        """
        with self.lock:
            if self.queue.full():
                try:
                    self.queue.get_nowait()
                except Empty:
                    pass

            self.queue.put(item)

    def get(self):
        """Retrieve latest item.

        Returns the most recent item if available.
        Returns None if buffer is empty.
        """
        with self.lock:
            try:
                return self.queue.get_nowait()
            except Empty:
                return None

    def clear(self):
        """Clear buffer.

        Removes all items from the buffer safely.
        Useful when resetting system state.
        """
        with self.lock:
            while not self.queue.empty():
                try:
                    self.queue.get_nowait()
                except Empty:
                    break

    def is_empty(self):
        """Check if buffer is empty.

        Returns True if buffer contains no items.
        """
        return self.queue.empty()