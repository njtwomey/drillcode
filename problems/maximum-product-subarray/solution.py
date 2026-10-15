"""Maximum Product Subarray (#152, medium)

Approach: Track both the max and min product ending at each index, since a negative
    swaps them.
Tricks: Including nums[i] itself as a candidate handles zeros without a special reset.
Edge cases:
  - Single negative
  - Zeros
  - Two negatives that cancel

Time O(n), space O(1).
"""


class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        cur_max = cur_min = best = nums[0]
        for num in nums[1:]:
            candidates = (num, cur_max * num, cur_min * num)
            cur_max = max(candidates)
            cur_min = min(candidates)
            best = max(best, cur_max)
        return best
