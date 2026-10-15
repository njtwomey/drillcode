"""Subsets II (#90, medium)

Approach: Sort, then backtrack over start indices, recording every path and skipping a
    value equal to its left neighbour at the same depth.
Tricks: Skip when i > start and nums[i] == nums[i-1]; the condition is i > start, not i
    > 0, or deeper picks of a repeated value are lost.
Edge cases:
  - All elements equal
  - Unsorted input with duplicates
  - Single element

Time O(n * 2^n), space O(n).
"""

class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        # Sorting puts equal values next to each other, so a duplicate can be
        # recognised by comparing with its left neighbour.
        nums.sort()
        result = []
        path = []

        def backtrack(start: int) -> None:
            # Every path, including the empty one, is a subset as soon as it exists.
            result.append(path[:])
            for i in range(start, len(nums)):
                # Choosing an equal value again as the "next element" at this depth would
                # rebuild subsets the first copy already produced. Later copies are still
                # reachable one level deeper, where they are not the first at that depth.
                if i > start and nums[i] == nums[i - 1]:
                    continue
                path.append(nums[i])
                backtrack(i + 1)
                path.pop()

        backtrack(0)
        return result
