"""Put values in a set; only from values with no predecessor (n - 1 absent) count upward.

Starting only at sequence starts is what keeps it linear.
Time O(n), space O(n).
"""


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        values = set(nums)
        best = 0
        for num in values:
            if num - 1 not in values:
                length = 1
                while num + length in values:
                    length += 1
                best = max(best, length)
        return best
