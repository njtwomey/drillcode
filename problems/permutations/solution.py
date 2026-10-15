"""Backtracking DFS: build a path, tracking used elements, and emit a copy of
the path when it reaches full length.

Time O(n * n!), space O(n) beyond the output.
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
