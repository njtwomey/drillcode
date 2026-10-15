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
        # tails[i] = smallest possible last value of an increasing subsequence of length
        # i + 1. Keeping tails small leaves the most room to extend later. It stays
        # sorted, so we can binary search it. Only its length is meaningful.
        tails = []
        for num in nums:
            # bisect_left finds the first tail >= num. Using left (not right) makes equal
            # values replace rather than extend, which enforces strictly increasing.
            i = bisect_left(tails, num)
            if i == len(tails):  # num beats every tail, so the longest run grows by one
                tails.append(num)
            else:
                tails[i] = num  # same length, but a smaller (better) ending value
        return len(tails)

    # Alternative: O(n^2) DP over earlier elements.
    def lengthOfLISQuadratic(self, nums: List[int]) -> int:
        # dp[i] = length of the longest increasing subsequence ending exactly at nums[i].
        dp = [1] * len(nums)
        for i in range(len(nums)):
            for j in range(i):
                if nums[j] < nums[i]:  # nums[i] can extend any smaller earlier ending
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp, default=0)  # the run may end anywhere; default covers empty input
