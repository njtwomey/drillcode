"""Random Pick with Weight (#528, medium)

Approach: Prefix sums of the weights, then binary search a uniform random target in
    1..total.
Tricks: Index i owns a block of w[i] consecutive targets, so a uniform target gives
    probability w[i] / total; bisect_left on targets 1..total avoids off-by-one.
Edge cases:
  - Single weight always returns 0
  - One very heavy weight next to light ones
  - Equal weights

Time O(n) constructor, O(log n) per pickIndex, space O(n).
"""

import random
from bisect import bisect_left
from itertools import accumulate


class Solution:
    def __init__(self, w: List[int]):
        # prefix[i] is the total weight of indices 0..i, so index i owns the
        # integer targets in (prefix[i-1], prefix[i]], a block of size w[i].
        self.prefix = list(accumulate(w))
        self.total = self.prefix[-1]

    def pickIndex(self) -> int:
        # A uniform target over 1..total lands in index i's block with
        # probability w[i] / total; binary search finds the block.
        target = random.randint(1, self.total)
        return bisect_left(self.prefix, target)
