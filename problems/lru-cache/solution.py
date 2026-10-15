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

# Judge notes:
# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key, value)


# Doubly linked list node: O(1) removal from the middle needs prev and next pointers.
class _Entry:
    def __init__(self, key=0, value=0):
        self.key = key  # stored so eviction can delete the dict entry from the node
        self.value = value
        self.prev = None
        self.next = None


# Dict gives O(1) lookup by key; the linked list keeps recency order (head = newest,
# tail = oldest). Dummy head and tail nodes mean unlink/insert never special-case ends.
class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.entries = {}
        self.head = _Entry()  # most recently used side
        self.tail = _Entry()  # least recently used side
        self.head.next = self.tail
        self.tail.prev = self.head

    # Splice entry out by joining its neighbours.
    def _unlink(self, entry):
        entry.prev.next = entry.next
        entry.next.prev = entry.prev

    # Insert right after the dummy head, marking entry as most recently used.
    def _push_front(self, entry):
        entry.next = self.head.next
        entry.prev = self.head
        self.head.next.prev = entry
        self.head.next = entry

    def get(self, key: int) -> int:
        entry = self.entries.get(key)
        if entry is None:
            return -1
        # A read counts as a use, so move it to the front.
        self._unlink(entry)
        self._push_front(entry)
        return entry.value

    def put(self, key: int, value: int) -> None:
        entry = self.entries.get(key)
        # Existing key: update in place and refresh recency. No eviction needed.
        if entry is not None:
            entry.value = value
            self._unlink(entry)
            self._push_front(entry)
            return
        # New key and cache is full: evict the least recently used (just before the tail).
        if len(self.entries) == self.capacity:
            oldest = self.tail.prev
            self._unlink(oldest)
            del self.entries[oldest.key]
        entry = _Entry(key, value)
        self.entries[key] = entry
        self._push_front(entry)
