Given an integer array `nums` and a window size `k`, slide a window of `k` consecutive elements from left to right, one position at a time. For each window position, compute the median of its values: the middle value when `k` is odd, or the mean of the two middle values when `k` is even.

Return the list of medians, one per window position, as floats. Answers within `10^-5` of the true value are accepted.

Constraints:
- `1 <= k <= len(nums) <= 10^5`
- `-2^31 <= nums[i] <= 2^31 - 1`
- Re-sorting every window is too slow for large `k`
