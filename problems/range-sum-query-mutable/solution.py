"""Range Sum Query - Mutable (#307, medium)

Approach: Fenwick tree (binary indexed tree) with point updates and prefix-sum
    differences.
Tricks: i & -i is the lowest set bit; adding it climbs to the next covering block and
    subtracting it hops to the previous block.
Edge cases:
  - Single element
  - Update to the same or a negative value
  - Queries spanning a single index

Time O(n) build, O(log n) per operation, space O(n).
"""

class NumArray:
    # Fenwick tree (binary indexed tree), 1-based. tree[i] stores the sum of the
    # block of elements ending at i whose length is the lowest set bit of i, i.e.
    # i & -i. For i = 6 (0b110) the block is 2 long: elements 5 and 6.
    def __init__(self, nums: List[int]):
        self.nums = list(nums)
        self.n = len(nums)
        self.tree = [0] * (self.n + 1)
        # Linear-time build: push each partial sum to its parent block, which is
        # the index plus its lowest set bit.
        for i in range(1, self.n + 1):
            self.tree[i] += nums[i - 1]
            parent = i + (i & -i)
            if parent <= self.n:
                self.tree[parent] += self.tree[i]

    def update(self, index: int, val: int) -> None:
        delta = val - self.nums[index]
        self.nums[index] = val
        # Adding the lowest set bit climbs to the next block that covers this index.
        i = index + 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i

    # Prefix sum of the first k elements. Subtracting the lowest set bit hops to the
    # block just before the one we added, so we visit at most log n disjoint blocks.
    def _prefix(self, k: int) -> int:
        total = 0
        while k > 0:
            total += self.tree[k]
            k -= k & -k
        return total

    def sumRange(self, left: int, right: int) -> int:
        return self._prefix(right + 1) - self._prefix(left)
