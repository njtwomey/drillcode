"""Partition Equal Subset Sum (#416, medium)

Approach: Subset-sum DP for target = total / 2 with a 1D boolean array iterated from
    high to low.
Tricks: Iterating downward uses each number at most once; an odd total is an immediate
    false.
Edge cases:
  - Odd total
  - Single element
  - One element equal to half the total

Time O(n · sum), space O(sum).
"""


class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        total = sum(nums)
        if total % 2:
            return False
        target = total // 2
        dp = [False] * (target + 1)
        dp[0] = True
        for num in nums:
            for s in range(target, num - 1, -1):
                if dp[s - num]:
                    dp[s] = True
        return dp[target]
