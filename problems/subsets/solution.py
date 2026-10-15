"""Subsets (#78, medium)

Approach: Include/exclude DFS per element, or iterate bitmasks 0..2^n - 1.
Tricks: The bitmask loop is the shortest to write.
Edge cases:
  - Empty input (result is [[]])

Time O(n · 2^n), space O(n).
"""


class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        # Each subset is an n-bit mask: bit i says whether nums[i] is included.
        # Counting 0 .. 2^n - 1 enumerates every combination exactly once.
        # (mask >> i & 1 parses as (mask >> i) & 1.)
        return [[nums[i] for i in range(n) if mask >> i & 1] for mask in range(1 << n)]

    # Alternative: include/exclude DFS, same time, O(n) recursion depth.
    def subsetsDfs(self, nums: List[int]) -> List[List[int]]:
        result = []
        path = []

        def dfs(i):
            # Every element has been decided: path is one finished subset.
            # Copy it, since backtracking keeps mutating the list.
            if i == len(nums):
                result.append(path[:])
                return
            dfs(i + 1)  # branch 1: skip nums[i]
            path.append(nums[i])
            dfs(i + 1)  # branch 2: take nums[i]
            path.pop()  # backtrack so the caller sees path unchanged

        dfs(0)
        return result
