"""Insert Delete GetRandom O(1) (#380, medium)

Approach: A list for random access plus a dict from value to list index.
Tricks: Remove by overwriting the hole with the last element then popping; update the
    moved element's index before deleting val so removing the last element still works.
Edge cases:
  - Remove the last element itself
  - Insert of an existing value and remove of a missing one
  - Set shrinks to one element or to empty and is refilled

Time O(1) average per operation, space O(n).
"""

# Judge notes:
# Your RandomizedSet object will be instantiated and called as such:
# obj = RandomizedSet()
# param_1 = obj.insert(val)
# param_2 = obj.remove(val)
# param_3 = obj.getRandom()
# Each element present must be returned by getRandom with equal probability.


import random


class RandomizedSet:
    def __init__(self):
        self.values = []  # random access by index gives O(1) getRandom
        self.pos = {}  # value -> its index in values, gives O(1) membership

    def insert(self, val: int) -> bool:
        if val in self.pos:
            return False
        self.pos[val] = len(self.values)
        self.values.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.pos:
            return False
        # Deleting from the middle of a list is O(n). Overwrite the hole with the
        # last element instead, then pop the tail.
        idx = self.pos[val]
        last = self.values[-1]
        self.values[idx] = last
        self.pos[last] = idx
        self.values.pop()
        del self.pos[val]  # after the update above so removing the last element works
        return True

    def getRandom(self) -> int:
        return random.choice(self.values)
