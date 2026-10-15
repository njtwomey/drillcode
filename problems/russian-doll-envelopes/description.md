You are given `envelopes`, a list of `[width, height]` pairs. One envelope fits inside another only if both its width and its height are strictly smaller than the other's. Rotating an envelope is not allowed. Return the largest number of envelopes that can be nested one inside the next, a chain of strictly increasing width and height.

Constraints:
- `1 <= len(envelopes) <= 10^5`
- `1 <= width, height <= 10^5`
- Envelopes may share a width, a height, or both
- Quadratic time is too slow at this size; aim for O(n log n)
