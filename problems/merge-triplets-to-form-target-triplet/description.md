You are given a list `triplets` of integer triples and a `target` triple. One operation picks two distinct triplets and replaces the second with their element-wise maximum, `[max(a0, b0), max(a1, b1), max(a2, b2)]`. You may perform any number of operations, including none. Return `True` if `target` can end up as one of the triplets in `triplets`, otherwise `False`.

Constraints:
- `1 <= len(triplets) <= 10^5`
- Every triplet and `target` has exactly 3 values, each in `[1, 1000]`
