"""Contiguous Array (#525, medium)

Approach: Map 0 to -1 and track a running balance; the longest span between two equal
    balances is the answer.
Tricks: Store only the first index of each balance and seed {0: -1} so subarrays
    starting at index 0 count.
Edge cases:
  - No balanced subarray (all ones or all zeros)
  - Whole array balanced
  - Best subarray begins at index 0

Time O(n), space O(n).
"""

class Solution:
    def findMaxLength(self, nums: List[int]) -> int:
        # Treat 0 as -1. A subarray has equal 0s and 1s exactly when its sum is 0, i.e.
        # when the running balance is the same at both ends.
        # first_seen maps balance -> earliest index at which it occurred. Balance 0 before
        # the array starts (index -1) lets a subarray begin at index 0.
        first_seen = {0: -1}
        balance = 0
        best = 0
        for i, num in enumerate(nums):
            balance += 1 if num == 1 else -1
            if balance in first_seen:
                # Same balance earlier: everything in between nets to zero.
                best = max(best, i - first_seen[balance])
            else:
                # Keep only the earliest index; it gives the longest span later.
                first_seen[balance] = i
        return best
