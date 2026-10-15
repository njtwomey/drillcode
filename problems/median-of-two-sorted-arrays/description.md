Given two sorted integer arrays `nums1` and `nums2`, return the median of all their elements combined, as a float. For an odd total count the median is the middle value of the merged order; for an even count it is the mean of the two middle values. Either array may be empty, but not both.

Constraints:
- `0 <= len(nums1), len(nums2) <= 1000`, and `len(nums1) + len(nums2) >= 1`
- `-10^6 <= nums1[i], nums2[i] <= 10^6`
- Both arrays are sorted in non-decreasing order
- The overall runtime must be O(log(m + n))
