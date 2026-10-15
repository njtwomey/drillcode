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
        candidates = sorted(candidates)
        result = []
        path = []

        def dfs(start, remaining):
            if remaining == 0:
                result.append(path[:])
                return
            for i in range(start, len(candidates)):
                c = candidates[i]
                if c > remaining:
                    break
                path.append(c)
                dfs(i, remaining - c)
                path.pop()

        dfs(0, target)
        return result
