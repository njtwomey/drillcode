You are given `intervals`, where `intervals[i] = [left, right]` is the inclusive range from `left` to `right`, and an integer array `queries`. An interval's size is `right - left + 1`.

For each `queries[j]`, find the size of the smallest interval that contains it (`left <= queries[j] <= right`), or `-1` if no interval does. Return the answers in the same order as `queries`, which may be unsorted and contain duplicates.

Constraints:
- `1 <= len(intervals), len(queries) <= 10^5`
- `1 <= left <= right <= 10^7`
- `1 <= queries[j] <= 10^7`
- A per-query scan of all intervals is too slow
