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
        return [[nums[i] for i in range(n) if mask >> i & 1] for mask in range(1 << n)]

    # Alternative: include/exclude DFS, same time, O(n) recursion depth.
    def subsetsDfs(self, nums: List[int]) -> List[List[int]]:
        result = []
        current = []

        def dfs(i):
            if i == len(nums):
                result.append(current[:])
                return
            dfs(i + 1)
            current.append(nums[i])
            dfs(i + 1)
            current.pop()

        dfs(0)
        return result
