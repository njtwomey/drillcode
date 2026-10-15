"""Permutations (#46, medium)

Approach: DFS building a path and tracking used elements; emit at full length.
Tricks: The swap-in-place variant avoids the used array.
Edge cases:
  - Single element

Time O(n · n!), space O(n).
"""


class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        result = []
        path = []
        used = [False] * len(nums)

        def dfs():
            if len(path) == len(nums):
                result.append(path[:])
                return
            for i, num in enumerate(nums):
                if used[i]:
                    continue
                used[i] = True
                path.append(num)
                dfs()
                path.pop()
                used[i] = False

        dfs()
        return result
