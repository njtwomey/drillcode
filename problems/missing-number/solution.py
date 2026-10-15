"""Missing Number (#268, easy)

Approach: XOR all indices and values, or subtract the sum from n(n+1)/2.
Tricks: XOR avoids any overflow concern; the sum version is easier to explain.
Edge cases:
  - Missing number is 0 or n

Time O(n), space O(1).
"""


class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        result = len(nums)
        for i, num in enumerate(nums):
            result ^= i ^ num
        return result

    # Alternative: expected sum n(n+1)/2 minus the actual sum.
    def missingNumberSum(self, nums: List[int]) -> int:
        n = len(nums)
        return n * (n + 1) // 2 - sum(nums)
