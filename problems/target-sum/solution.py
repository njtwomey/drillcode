"""Target Sum (#494, medium)

Approach: Reduce to counting subsets that sum to (total + target) / 2 and run a 0/1
    knapsack count with a 1D array.
Tricks: Iterate sums downward so each number is used once; return 0 when |target|
    exceeds the total or the parity is odd, and zeros double the count.
Edge cases:
  - Zeros (each doubles the count)
  - Target beyond the total or of the wrong parity
  - Negative target

Time O(n·S), space O(S).
"""

class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        # Let P be the numbers given '+' and N those given '-'. Then
        #   sum(P) - sum(N) = target   and   sum(P) + sum(N) = total,
        # so sum(P) = (total + target) / 2. The task becomes: count subsets of nums whose
        # sum is exactly goal. That is a 0/1 knapsack counting problem.
        total = sum(nums)
        # Impossible if the target is out of reach or total + target is odd.
        if abs(target) > total or (total + target) % 2:
            return 0
        goal = (total + target) // 2

        # dp[s] = number of subsets of the numbers seen so far that sum to s.
        # Base case: dp[0] = 1, the empty subset.
        dp = [0] * (goal + 1)
        dp[0] = 1

        # Each number is used at most once, so s runs DOWNWARD: dp[s - num] must still
        # describe the state before this number was considered. A zero gives
        # dp[s] += dp[s], doubling the counts (it can be '+0' or '-0'), which is correct.
        for num in nums:
            for s in range(goal, num - 1, -1):
                dp[s] += dp[s - num]
        return dp[goal]
