Given a circular integer array `nums` (after the last element comes the first again), return an array `result` of the same length where `result[i]` is the first value strictly greater than `nums[i]` found by walking forward from index `i`, wrapping around the end if needed. If no element in the whole circle is greater, `result[i]` is `-1`.

Constraints:
- `1 <= len(nums) <= 10^4`
- `-10^9 <= nums[i] <= 10^9`
- Duplicates are allowed
- A solution that scans forward for every index is O(n^2)
