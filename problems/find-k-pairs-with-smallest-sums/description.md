You are given two integer arrays `nums1` and `nums2`, each sorted in non-decreasing order, and an integer `k`. A pair `[u, v]` takes one value `u` from `nums1` and one value `v` from `nums2`. Return the `k` pairs with the smallest sums `u + v`, or all pairs if fewer than `k` exist.

Pairs with equal sums may be returned in any order. Pairs formed from different indices with equal values count separately.

Constraints:
- `1 <= len(nums1), len(nums2) <= 10^5`
- Values are in `[-10^9, 10^9]`
- `1 <= k <= 10^4`
- Enumerating all `len(nums1) * len(nums2)` pairs is too slow
