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
        # Two equal halves need an even total.
        if total % 2:
            return False
        # Reduced to 0/1 knapsack: is there a subset summing to half the total?
        # The other subset then automatically sums to the other half.
        target = total // 2
        # dp[s] means some subset of the numbers seen so far sums to exactly s.
        dp = [False] * (target + 1)
        dp[0] = True  # the empty subset
        for num in nums:
            # Go downward so dp[s - num] still reflects the state BEFORE this num.
            # Going upward would let the same num be reused several times.
            # Stopping at num avoids a negative index.
            for s in range(target, num - 1, -1):
                if dp[s - num]:
                    dp[s] = True
        return dp[target]
