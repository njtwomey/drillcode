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
        result = [1] * n
        # Answer[i] = (product of everything left of i) * (product right of i).
        # Pass 1 fills in the left part. The product is taken before multiplying in
        # nums[i], so index i itself is excluded.
        prefix = 1
        for i in range(n):
            result[i] = prefix
            prefix *= nums[i]
        # Pass 2 multiplies in the right part with one running variable, walking
        # backwards. Reusing result as storage keeps extra space O(1) (output excluded).
        # No division, so zeros need no special handling.
        suffix = 1
        for i in range(n - 1, -1, -1):
            result[i] *= suffix
            suffix *= nums[i]
        return result
