---
title: Fenwick tree
area: Design
topics: [Design, Array]
problems:
  - range-sum-query-immutable
  - range-sum-query-mutable
related: [design-structures, bit-tricks, dp-space-and-loop-order]
---
## Reach for it when

- Many range-sum (or prefix-sum) queries are mixed with point updates.
- A plain prefix array would be right, but a value changes between queries and rebuilding it costs O(n) per update.
- The statement is a class with `update` and `sumRange`, or any "count of values below x so far" that grows over time.
- The operation has an inverse (sum and count do; min and max do not).

## Setup

- `tree = [0] * (n + 1)`: 1-based. Index 0 is unused so that `i & -i` never sees 0. Invariant: `tree[i]` is the sum of the block of elements that ends at `i` and is `i & -i` long. For `i = 6` (binary 110) that is elements 5 and 6.
- `nums`: a copy of the current values. An update adds `val - nums[index]` to the tree, so the old value must be known.
- `i + (i & -i)`: the next block that covers index `i`. Climb with it on update.
- `k - (k & -k)`: the block just before the one at `k`. Hop with it on query, so at most log n disjoint blocks are added.
- Convert once at the edges: the public index is 0-based, the tree index is `index + 1`, and `_prefix(k)` sums the first `k` elements.
- Build in O(n) by pushing each `tree[i]` to its parent `i + (i & -i)`, instead of n separate updates.

## Template

```python
def fenwick_demo(nums, updates, queries):
    n = len(nums)
    tree = [0] * (n + 1)
    for i in range(1, n + 1):
        tree[i] += nums[i - 1]
        parent = i + (i & -i)
        if parent <= n:
            tree[parent] += tree[i]

    def prefix(k):
        total = 0
        while k > 0:
            total += tree[k]
            k -= k & -k
        return total

    def update(index, delta):
        i = index + 1
        while i <= n:
            tree[i] += delta
            i += i & -i

    for index, delta in updates:
        update(index, delta)
    return [prefix(right + 1) - prefix(left) for left, right in queries]
```

`fenwick_demo([1, 3, 5], [(1, 2)], [(0, 2), (1, 1)])` returns `[11, 5]`: after adding 2 at index 1 the array is `[1, 5, 5]`. A range sum is two prefix sums subtracted, as with a prefix array.

## What it removes

- The O(n) rebuild of a prefix array after each update. An update touches at most log n blocks.
- The O(n) scan per query that a plain array with point updates needs. A query adds at most log n blocks.
- A segment tree's node objects and recursion, for the sum case. The tree is one flat list and two short loops.

## Pitfalls

- Using index 0. `0 & -0` is 0, so `i += i & -i` never moves and the update loops forever. Keep the tree 1-based and add 1 to the public index.
- Passing the new value instead of the difference to the tree. The tree stores sums, so the update adds `val - nums[index]`. Without the stored `nums`, repeated updates to one index drift.
- Forgetting to write the new value into `nums` too. The next update's delta is then computed from the old value.
- `sumRange(left, right)` as `prefix(right) - prefix(left)`. That drops `nums[right]`. Use `prefix(right + 1) - prefix(left)`.
- Mixing the two directions: `+=` on query or `-=` on update. Updates climb up with `+ (i & -i)`, queries hop down with `- (i & -i)`.
- Sizing the tree `n` instead of `n + 1`. The last element has no slot.
- Using a Fenwick tree when the data never changes. A prefix array answers in O(1) and takes fewer lines.

## Variants

- Immutable data, `range-sum-query-immutable`: no tree. `prefix = [0]`, then append `prefix[-1] + num`; a query is `prefix[right + 1] - prefix[left]`. O(n) to build, O(1) per query. The leading 0 removes the special case for a range that starts at index 0. Use this whenever nothing is updated.
- Mutable data, `range-sum-query-mutable`: the Fenwick tree above, with `update(index, val)` computing the delta from `self.nums`. O(n) build, O(log n) update, O(log n) query.
- Other uses of the same walk (not in this catalogue): count of elements below a value, by indexing the tree on the value's rank and adding 1 per element; inversion counts.

## Worked example

Problem: `range-sum-query-mutable`

A Fenwick tree with a linear build, a delta update that climbs by the lowest set bit, and a prefix query that hops down by it.

```python
class NumArray:

    def __init__(self, nums: List[int]):
        self.nums = list(nums)
        self.n = len(nums)
        self.tree = [0] * (self.n + 1)
        for i in range(1, self.n + 1):
            self.tree[i] += nums[i - 1]
            parent = i + (i & -i)
            if parent <= self.n:
                self.tree[parent] += self.tree[i]

    def update(self, index: int, val: int) -> None:
        delta = val - self.nums[index]
        self.nums[index] = val
        i = index + 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i

    def _prefix(self, k: int) -> int:
        total = 0
        while k > 0:
            total += self.tree[k]
            k -= k & -k
        return total

    def sumRange(self, left: int, right: int) -> int:
        return self._prefix(right + 1) - self._prefix(left)
```

`self.tree` is the 1-based `tree` from Setup, and the constructor is the linear build from the Template. In `update`, `delta` is the change and `i = index + 1` moves to tree numbering; `i += i & -i` climbs through every block that contains the index. `_prefix` is the template's `prefix`: `k -= k & -k` drops the lowest set bit each round, so the blocks it adds do not overlap. `sumRange` subtracts two prefixes.
