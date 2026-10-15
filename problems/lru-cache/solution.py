"""Hash map plus doubly linked list with sentinel head and tail nodes.

A hit moves the node to the front; put evicts from the tail when over capacity.
All operations O(1); space O(capacity).
"""


class _Entry:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.entries = {}
        self.head = _Entry()  # most recently used side
        self.tail = _Entry()  # least recently used side
        self.head.next = self.tail
        self.tail.prev = self.head

    def _unlink(self, entry):
        entry.prev.next = entry.next
        entry.next.prev = entry.prev

    def _push_front(self, entry):
        entry.next = self.head.next
        entry.prev = self.head
        self.head.next.prev = entry
        self.head.next = entry

    def get(self, key: int) -> int:
        entry = self.entries.get(key)
        if entry is None:
            return -1
        self._unlink(entry)
        self._push_front(entry)
        return entry.value

    def put(self, key: int, value: int) -> None:
        entry = self.entries.get(key)
        if entry is not None:
            entry.value = value
            self._unlink(entry)
            self._push_front(entry)
            return
        if len(self.entries) == self.capacity:
            oldest = self.tail.prev
            self._unlink(oldest)
            del self.entries[oldest.key]
        entry = _Entry(key, value)
        self.entries[key] = entry
        self._push_front(entry)
