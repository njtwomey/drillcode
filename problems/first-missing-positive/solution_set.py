"""Put everything in a set and probe 1, 2, 3, ... until one is absent.

Simple and does not mutate the input. Time O(n), space O(n).
"""


class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        seen = set(nums)
        # At most n positives can be present, so the loop ends by n + 1.
        candidate = 1
        while candidate in seen:
            candidate += 1
        return candidate
