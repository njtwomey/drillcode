"""Longest Increasing Subsequence (#300, medium)

Approach: O(n²) DP over earlier elements, or O(n log n) with a tails array and binary
    search.
Tricks: In the tails array replace the first element >= x; its length is the answer but
    its contents are not the subsequence.
Edge cases:
  - Strictly decreasing input (answer 1)
  - Duplicates do not extend a strictly increasing run

Time O(n log n), space O(n).
"""
from bisect import bisect_left


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        tails = []
        for num in nums:
            i = bisect_left(tails, num)
            if i == len(tails):
                tails.append(num)
            else:
                tails[i] = num
        return len(tails)

    # Alternative: O(n^2) DP over earlier elements.
    def lengthOfLISQuadratic(self, nums: List[int]) -> int:
        dp = [1] * len(nums)
        for i in range(len(nums)):
            for j in range(i):
                if nums[j] < nums[i]:
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp, default=0)
