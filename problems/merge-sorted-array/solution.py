"""Merge Sorted Array (#88, easy)

Approach: Merge from the back with pointers at the last real element of each array,
    writing the larger into the free tail of nums1.
Tricks: Filling from the back never overwrites unread values of nums1, and once nums2 is
    exhausted the rest is already in place.
Edge cases:
  - n = 0 so nums1 is unchanged
  - m = 0 so nums2 is copied over
  - All of nums2 smaller or larger than nums1
  - Duplicates and negatives

Time O(m + n), space O(1).
"""

# Judge notes:
# Do not return anything: modify nums1 in place instead.


class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        # Fill nums1 from the back. The free space sits at the end, so writing the
        # largest remaining value there can never overwrite an unread element of nums1.
        i, j = m - 1, n - 1  # last unmerged element of nums1 and of nums2
        for k in range(m + n - 1, -1, -1):
            # Once nums2 is used up, the rest of nums1 is already in place.
            if j < 0:
                break
            if i >= 0 and nums1[i] > nums2[j]:
                nums1[k] = nums1[i]
                i -= 1
            else:
                nums1[k] = nums2[j]
                j -= 1
