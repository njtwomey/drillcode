"""Snapshot Array (#1146, medium)

Approach: Per-index list of (snap id, value) changes, binary searched by snap id on get.
Tricks: Never copy the array on snap; overwrite the last entry when the index is set
    twice in the same snap, and use bisect_right minus one so untouched snaps read the
    earlier value.
Edge cases:
  - Index never set reads 0
  - Several sets between two snaps
  - Snaps in which an index is not touched
  - Setting a value back to 0

Time O(1) set and snap, O(log s) get, space O(number of sets).
"""

# Judge notes:
# Your SnapshotArray object will be instantiated and called as such:
# obj = SnapshotArray(length)
# obj.set(index, val)
# param_1 = obj.snap()
# param_2 = obj.get(index, snap_id)


from bisect import bisect_right


class SnapshotArray:
    def __init__(self, length: int):
        self.snap_id = 0
        # Copying the whole array on every snap would cost O(length) each time.
        # Instead each index keeps only its changes, as (snap_id, value) in
        # increasing snap_id order. Everything starts as 0 at snap 0.
        self.history = [[(0, 0)] for _ in range(length)]

    def set(self, index: int, val: int) -> None:
        changes = self.history[index]
        if changes[-1][0] == self.snap_id:
            changes[-1] = (self.snap_id, val)  # several sets before one snap: keep the last
        else:
            changes.append((self.snap_id, val))

    def snap(self) -> int:
        self.snap_id += 1
        return self.snap_id - 1

    def get(self, index: int, snap_id: int) -> int:
        # The value at snap_id is the latest change recorded at or before it,
        # which also covers snaps where this index was not touched.
        changes = self.history[index]
        pos = bisect_right(changes, snap_id, key=lambda change: change[0])
        return changes[pos - 1][1]
