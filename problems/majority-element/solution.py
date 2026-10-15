"""Majority Element (#169, easy)

Approach: Boyer-Moore voting: keep a candidate and a count, decrement on mismatch,
    replace at zero.
Tricks: Correct only because a majority element is guaranteed to exist.
Edge cases:
  - Single element
  - Majority element clustered at the end

Time O(n), space O(1).
"""


class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        # Boyer-Moore: each non-majority vote cancels one majority vote. The majority
        # appears more than n/2 times, so it cannot be fully cancelled and survives.
        candidate, count = 0, 0
        for num in nums:
            if count == 0:  # Everything so far cancelled out; start fresh with this value.
                candidate = num
            count += 1 if num == candidate else -1
        return candidate
