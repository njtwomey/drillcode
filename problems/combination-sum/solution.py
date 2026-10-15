"""DFS choosing candidates from index i onward, allowing the same index to be reused.

Passing the start index prevents duplicate orderings; sorting lets us prune once a candidate exceeds the remainder.
Time O(N^(T/M)), space O(T/M) recursion depth.
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
