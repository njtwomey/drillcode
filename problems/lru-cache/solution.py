"""LRU Cache (#146, medium)

Approach: Hash map plus doubly linked list; move a node to the front on access, evict
    from the tail.
Tricks: Sentinel head and tail nodes remove null checks; OrderedDict in Python does the
    same job.
Edge cases:
  - Capacity 1
  - Put of an existing key updates and refreshes it
  - Get of a missing key

Time O(1) per operation, space O(capacity).
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
