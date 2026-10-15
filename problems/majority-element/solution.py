"""Boyer-Moore voting: keep a candidate and a count, decrement on mismatch, replace at zero.

Correct only because a majority element is guaranteed to exist.
Time O(n), space O(1).
"""


class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        candidate, count = 0, 0
        for num in nums:
            if count == 0:
                candidate = num
            count += 1 if num == candidate else -1
        return candidate
