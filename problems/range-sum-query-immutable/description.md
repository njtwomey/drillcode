Implement `NumArray`, a structure over a fixed integer list that answers range-sum queries.

- `NumArray(nums)`: build the structure from the list `nums`, which never changes afterwards.
- `sumRange(left, right)`: return the sum of `nums[left]` through `nums[right]`, both inclusive. `left <= right` and both are valid indices.

Constraints:
- `1 <= len(nums) <= 10^4`
- `-10^5 <= nums[i] <= 10^5`
- Up to `10^4` calls to `sumRange`, so each query should be O(1)
