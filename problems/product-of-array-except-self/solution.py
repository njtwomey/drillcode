"""Write prefix products into the output array, then multiply by a running
suffix product in a second pass. No division, so zeros need no special case.

Time O(n), space O(1) extra (output excluded).
"""


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        out = [1] * n
        prefix = 1
        for i in range(n):
            out[i] = prefix
            prefix *= nums[i]
        suffix = 1
        for i in range(n - 1, -1, -1):
            out[i] *= suffix
            suffix *= nums[i]
        return out
