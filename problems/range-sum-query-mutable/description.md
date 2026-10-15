Implement `NumArray`, which holds an integer array and supports range sums interleaved with point updates.

- `NumArray(nums)`: initialise with the list `nums`.
- `update(index, val)`: set `nums[index]` to `val`. Returns nothing.
- `sumRange(left, right)`: return the sum of `nums[left..right]`, inclusive.

Indices are 0-based and always valid, with `left <= right`.

Constraints:
- `1 <= len(nums) <= 3 * 10^4`
- `-100 <= nums[i], val <= 100`
- Up to `3 * 10^4` calls in total, so both operations should be sub-linear
