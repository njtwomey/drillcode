"""Combination Sum II (#40, medium)

Approach: Sort, then backtrack with start index i + 1 for single use, skipping repeated
    values at the same depth and breaking once a candidate exceeds the remainder.
Tricks: Skip duplicates with i > start (not i > 0), and break rather than continue when
    the sorted candidate is too large.
Edge cases:
  - No combination reaches the target
  - Many equal candidates
  - Target smaller than every candidate

Time O(2^n), space O(n).
"""

class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        # Sorted order gives two things: equal values are adjacent (for duplicate
        # skipping) and once one candidate is too big every later one is too.
        candidates.sort()
        result = []
        path = []

        def backtrack(start: int, remaining: int) -> None:
            if remaining == 0:
                result.append(path[:])
                return
            for i in range(start, len(candidates)):
                if candidates[i] > remaining:
                    break
                # Each element is used at most once, so we always recurse on i + 1.
                # Among equal values at the same depth only the first may start a
                # branch; otherwise the same combination is generated several times.
                if i > start and candidates[i] == candidates[i - 1]:
                    continue
                path.append(candidates[i])
                backtrack(i + 1, remaining - candidates[i])
                path.pop()

        backtrack(0, target)
        return result
