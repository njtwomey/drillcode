"""Maintain a tails array (tails[i] = smallest tail of an increasing run of length i + 1);
binary search the first tail >= x and replace it, or append if none.

The length of tails is the answer, but its contents are not the subsequence.
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
