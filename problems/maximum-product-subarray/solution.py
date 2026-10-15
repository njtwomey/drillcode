"""Track the max and min product of a subarray ending at each index, since a
negative number swaps them. Starting each candidate from nums[i] itself handles zeros.

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
