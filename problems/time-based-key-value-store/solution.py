"""Time Based Key-Value Store (#981, medium)

Approach: Map each key to parallel lists of timestamps and values, and bisect_right the
    timestamps on get.
Tricks: Timestamps arrive in increasing order, so appending keeps each list sorted and
    no re-sorting is needed.
Edge cases:
  - Unknown key returns an empty string
  - Query earlier than the first timestamp
  - Query exactly at a stored timestamp
  - Query after the last timestamp

Time O(1) set, O(log n) get, space O(n).
"""

# Judge notes:
# Your TimeMap object will be instantiated and called as such:
# obj = TimeMap()
# obj.set(key, value, timestamp)
# param_1 = obj.get(key, timestamp)


from bisect import bisect_right


class TimeMap:
    def __init__(self):
        # key -> (timestamps, values), two parallel lists. set() is only called with
        # increasing timestamps, so each timestamps list stays sorted by construction.
        self.store = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        times, values = self.store.setdefault(key, ([], []))
        times.append(timestamp)
        values.append(value)

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.store:
            return ""
        times, values = self.store[key]
        # bisect_right gives the count of timestamps <= the query, so the entry just
        # before that position is the latest one not after it. Zero means every stored
        # timestamp is later than the query.
        idx = bisect_right(times, timestamp)
        return values[idx - 1] if idx else ""
