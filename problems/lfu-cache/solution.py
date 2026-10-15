"""LFU Cache (#460, hard)

Approach: Maps for value and frequency plus a per-frequency OrderedDict of keys,
    tracking the minimum frequency.
Tricks: A new key resets min_freq to 1, and a touch bumps min_freq only if it emptied
    the lowest bucket.
Edge cases:
  - Capacity 0 stores nothing
  - Capacity 1
  - Ties on frequency evict the least recently used
  - Put on an existing key counts as a use

Time O(1) per operation, space O(capacity).
"""

from collections import defaultdict, OrderedDict


# Three tables give O(1) everything:
#   values[key]    -> value
#   freq[key]      -> number of uses so far
#   buckets[f]     -> OrderedDict of keys used exactly f times, oldest first
# min_freq tracks the lowest non-empty bucket, so the eviction victim is the first key
# of buckets[min_freq]: least frequently used, ties broken by least recently used.
class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.values = {}
        self.freq = {}
        self.buckets = defaultdict(OrderedDict)
        self.min_freq = 0

    # Count one more use of key: move it from bucket f to bucket f + 1, at the
    # recent end (OrderedDict keeps insertion order).
    def _touch(self, key: int) -> None:
        f = self.freq[key]
        del self.buckets[f][key]
        # If we just emptied the lowest bucket, key itself now sits in f + 1, which
        # is therefore the new minimum.
        if not self.buckets[f]:
            del self.buckets[f]
            if self.min_freq == f:
                self.min_freq = f + 1
        self.freq[key] = f + 1
        self.buckets[f + 1][key] = None

    def get(self, key: int) -> int:
        if key not in self.values:
            return -1
        self._touch(key)
        return self.values[key]

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return
        if key in self.values:
            self.values[key] = value
            self._touch(key)
            return
        # New key at capacity: evict the oldest key in the lowest-frequency bucket.
        if len(self.values) == self.capacity:
            victim, _ = self.buckets[self.min_freq].popitem(last=False)
            if not self.buckets[self.min_freq]:
                del self.buckets[self.min_freq]
            del self.values[victim]
            del self.freq[victim]
        # A brand new key has frequency 1, which is always the minimum now.
        self.values[key] = value
        self.freq[key] = 1
        self.buckets[1][key] = None
        self.min_freq = 1
