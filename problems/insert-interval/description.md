`intervals` is a list of non-overlapping `[start, end]` intervals sorted by `start`, and `newInterval` is another interval. Insert `newInterval` and merge any overlapping intervals (intervals that touch at an endpoint overlap). Return the resulting sorted list of non-overlapping intervals.

Constraints:
- `0 <= len(intervals) <= 10^4`
- `0 <= start <= end <= 10^5`
- Aim for linear time.
