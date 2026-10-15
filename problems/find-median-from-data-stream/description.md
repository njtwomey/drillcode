Implement `MedianFinder`, which maintains a growing collection of integers.

- `MedianFinder()` creates an empty collection.
- `addNum(num)` inserts the integer `num`; returns nothing.
- `findMedian()` returns the median of all numbers added so far as a float: the middle value if the count is odd, or the mean of the two middle values if even. It is only called when at least one number has been added.

Constraints:
- Values lie in [-10^5, 10^5]
- Up to 5 * 10^4 calls in total
- Calls may be interleaved arbitrarily, so each should be efficient
