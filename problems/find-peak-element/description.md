Given an integer array `nums`, return the index of any peak element. A peak is an element strictly greater than both of its neighbours; the positions just before index `0` and just after the last index are treated as negative infinity, so an end element needs to beat only its single real neighbour.

If there are several peaks, returning the index of any one of them is accepted. Adjacent elements are never equal.

Constraints:
- `1 <= len(nums) <= 1000`
- `-2^31 <= nums[i] <= 2^31 - 1`
- `nums[i] != nums[i + 1]` for every valid `i`
- The solution must run in O(log n) time
