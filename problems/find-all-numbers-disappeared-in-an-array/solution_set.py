"""Build a set of the values present and list every number in 1..n missing from it.

Simple but needs extra space. Time O(n), space O(n).
"""


class Solution:
    def findDisappearedNumbers(self, nums: List[int]) -> List[int]:
        seen = set(nums)
        return [v for v in range(1, len(nums) + 1) if v not in seen]
