"""Missing Number (#268, easy)

Approach: XOR all indices and values, or subtract the sum from n(n+1)/2.
Tricks: XOR avoids any overflow concern; the sum version is easier to explain.
Edge cases:
  - Missing number is 0 or n

Time O(n), space O(1).
"""


class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        # x ^ x = 0 and XOR is order-independent. Start with n, then XOR every index 0..n-1
        # and every value. Each present number cancels with its index; the missing one is left.
        # Starting with n covers the case where the missing number is n (no index for it).
        result = len(nums)
        for i, num in enumerate(nums):
            result ^= i ^ num
        return result

    # Alternative: expected sum n(n+1)/2 minus the actual sum.
    def missingNumberSum(self, nums: List[int]) -> int:
        # Numbers 0..n sum to n(n+1)/2; the shortfall is the missing number.
        n = len(nums)
        return n * (n + 1) // 2 - sum(nums)
