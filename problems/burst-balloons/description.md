You are given balloons in a row, `nums[i]` being the number painted on balloon `i`. Bursting balloon `i` earns `left * nums[i] * right` coins, where `left` and `right` are the numbers on its current adjacent balloons; a missing neighbour past either end counts as 1. After a burst the row closes up. Return the maximum coins obtainable by bursting all balloons in the best order.

Constraints:
- `1 <= len(nums) <= 300`
- `0 <= nums[i] <= 100`
- Trying all burst orders is factorial; about O(n^3) time is expected
