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
        path = []  # the permutation being built; shared and mutated by backtracking
        used = [False] * len(nums)  # used[i]: nums[i] is already in path

        def dfs():
            # A full-length path is a complete permutation. Copy it, because path
            # keeps changing as we backtrack.
            if len(path) == len(nums):
                result.append(path[:])
                return
            # Try every unused element in this position. Looping from 0 each time
            # (rather than from a start index) is what yields all orderings.
            for i, num in enumerate(nums):
                if used[i]:
                    continue
                used[i] = True
                path.append(num)
                dfs()
                # Undo the choice so the next sibling starts from the same state.
                path.pop()
                used[i] = False

        dfs()
        return result
