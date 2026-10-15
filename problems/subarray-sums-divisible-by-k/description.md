Given an integer array `nums` and an integer `k`, return the number of non-empty contiguous subarrays whose sum is divisible by `k`. Subarrays are counted by position, so identical values at different places each count.

Elements may be negative or zero.

Constraints:
- `1 <= len(nums) <= 3 * 10^4`
- `-10^4 <= nums[i] <= 10^4`
- `2 <= k <= 10^4`
- Checking every subarray is too slow at the upper limit
