"""Product of Array Except Self (#238, medium)

Approach: Prefix products into the output array, then multiply by a running suffix
    product in a second pass.
Tricks: No division; the suffix pass needs only one variable, keeping extra space O(1).
Edge cases:
  - One zero
  - Two zeros
  - Negative numbers

Time O(n), space O(1).
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
