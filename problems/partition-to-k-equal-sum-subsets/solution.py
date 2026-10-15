"""Partition to K Equal Sum Subsets (#698, medium)

Approach: Bitmask DP where each reachable subset stores its total modulo target, and the
    full mask must end at remainder 0.
Tricks: Storing the sum modulo target makes the current bucket implicit, so no bucket
    index is needed.
Edge cases:
  - k = 1
  - Total not divisible by k
  - An element larger than the target

Time O(n * 2^n), space O(2^n).
"""

class Solution:
    def canPartitionKSubsets(self, nums: List[int], k: int) -> bool:
        total = sum(nums)
        if total % k:
            return False
        target = total // k
        if max(nums) > target:  # such an element fits in no bucket
            return False
        n = len(nums)
        # fill[mask] = total of the chosen numbers modulo target, or -1 if the subset
        # cannot be laid out as some full buckets plus one partly filled bucket.
        # Keeping only the remainder means "the current bucket" needs no extra state.
        fill = [-1] * (1 << n)
        fill[0] = 0
        for mask in range(1 << n):
            if fill[mask] < 0:
                continue
            for i in range(n):
                if mask >> i & 1:
                    continue
                # Adding nums[i] must not overflow the current bucket; reaching exactly
                # target wraps to 0, which starts a fresh bucket.
                if fill[mask] + nums[i] <= target:
                    fill[mask | 1 << i] = (fill[mask] + nums[i]) % target
        return fill[(1 << n) - 1] == 0
