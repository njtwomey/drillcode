"""Combination Sum (#39, medium)

Approach: DFS choosing candidates from index i onward, allowing the same index to be
    reused.
Tricks: Passing the start index prevents duplicate orderings; prune when the remainder
    goes negative.
Edge cases:
  - Target smaller than every candidate (empty result)

Time O(N^(T/M)), space O(T/M).
"""


class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        # Sorted so we can stop scanning as soon as one candidate is too large.
        candidates = sorted(candidates)
        result = []
        path = []  # the combination under construction (shared, so copy when saving)

        # Choose candidates from index start onward only. Never going back to earlier
        # indices means [2,3] and [3,2] are not both produced.
        def dfs(start, remaining):
            if remaining == 0:
                result.append(path[:])
                return
            for i in range(start, len(candidates)):
                c = candidates[i]
                # Larger candidates after this are bigger still, so prune the whole loop.
                if c > remaining:
                    break
                path.append(c)
                dfs(i, remaining - c)  # pass i, not i + 1: a number may be reused
                path.pop()

        dfs(0, target)
        return result
