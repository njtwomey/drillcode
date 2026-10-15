Given an integer array `nums` and an integer `k`, decide whether `nums` can be divided into `k` non-empty groups whose sums are all equal. Every element must belong to exactly one group.

Return `True` if such a division exists and `False` otherwise.

Constraints:
- `1 <= k <= len(nums) <= 16`
- `1 <= nums[i] <= 10^4`
- Plain backtracking over all assignments is exponential; the small `len(nums)` limit is the hint about acceptable cost
