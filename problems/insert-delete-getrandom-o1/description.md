Implement a class `RandomizedSet` that stores a set of distinct integers, with every operation running in O(1) average time.

- `insert(val)` adds `val` if it is not present and returns `true`; otherwise it returns `false`.
- `remove(val)` deletes `val` if it is present and returns `true`; otherwise it returns `false`.
- `getRandom()` returns one of the current elements, each with equal probability.

`getRandom` is only called while the set holds at least one element.

Constraints:
- `-2^31 <= val <= 2^31 - 1`
- At most `2 * 10^5` calls in total
- Each operation must be O(1) on average
