Given an integer array `nums`, return the maximum value of `nums[i] XOR nums[j]` over all index pairs with `0 <= i <= j < len(nums)`. Pairing an element with itself is allowed, which yields 0, so a one-element array returns 0.

Comparing every pair is too slow for the largest inputs; aim for time linear in `len(nums)` times the bit width.

Constraints:
- `1 <= len(nums) <= 2 * 10^5`
- `0 <= nums[i] <= 2^31 - 1`
