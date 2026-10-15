Given an array `heights` where each element is the height of a histogram bar of width 1, return the area of the largest axis-aligned rectangle that fits entirely inside the histogram. The rectangle must be built from consecutive bars, and its height is limited by the shortest bar it covers.

Constraints:
- `1 <= len(heights) <= 10^5`
- `0 <= heights[i] <= 10^4`
- A quadratic scan over all pairs of bars is too slow at this size
