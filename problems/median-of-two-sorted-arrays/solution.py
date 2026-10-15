"""Median of Two Sorted Arrays (#4, hard)

Approach: Binary search a partition of the shorter array so the combined left half has
    (m + n + 1) // 2 elements and max(left) <= min(right).
Tricks: Search the shorter array, and use -inf and inf for empty sides so the boundary
    comparisons need no special cases.
Edge cases:
  - One array empty
  - Even versus odd total length
  - Arrays that do not overlap at all
  - Very different lengths

Time O(log min(m, n)), space O(1).
"""

class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        # Binary search on the shorter array keeps the search range as small as possible
        # and guarantees the matching cut in the longer one never goes out of bounds.
        a, b = nums1, nums2
        if len(a) > len(b):
            a, b = b, a
        m, n = len(a), len(b)
        # Cut both arrays so the left parts together hold half the elements (one extra
        # on the left when the total is odd). The cut is right when every element on the
        # left is <= every element on the right.
        half = (m + n + 1) // 2
        lo, hi = 0, m
        while lo <= hi:
            i = (lo + hi) // 2  # how many elements of a go to the left side
            j = half - i  # the rest of the left side comes from b
            # The elements next to the cuts; infinity stands in when a side is empty.
            a_left = a[i - 1] if i > 0 else float("-inf")
            a_right = a[i] if i < m else float("inf")
            b_left = b[j - 1] if j > 0 else float("-inf")
            b_right = b[j] if j < n else float("inf")
            if a_left > b_right:
                hi = i - 1  # took too many from a: move its cut left
            elif b_left > a_right:
                lo = i + 1  # took too few from a: move its cut right
            else:
                # Valid cut: the median sits at the boundary.
                if (m + n) % 2:
                    return float(max(a_left, b_left))
                return (max(a_left, b_left) + min(a_right, b_right)) / 2
        return 0.0  # unreachable for sorted input
