"""Permutations II (#47, medium)

Approach: Backtrack over a counter of remaining copies, trying each distinct value once
    per position.
Tricks: Iterating distinct values with counts avoids duplicate permutations without
    sorting or a used array.
Edge cases:
  - All elements equal
  - Single element
  - Several repeated values

Time O(n * n!), space O(n).
"""

from collections import Counter


class Solution:
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        # Build permutations from a multiset: at each position try every distinct
        # value that still has copies left. Equal values are never tried twice at
        # the same position, so no duplicate permutation can appear.
        count = Counter(nums)
        result = []
        path = []

        def backtrack() -> None:
            if len(path) == len(nums):
                result.append(path[:])
                return
            for value in count:  # keys are distinct values; only the counts change
                if count[value] == 0:
                    continue
                count[value] -= 1
                path.append(value)
                backtrack()
                path.pop()
                count[value] += 1

        backtrack()
        return result
