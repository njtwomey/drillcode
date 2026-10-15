"""Rotate Array (#189, medium)

Approach: Reverse the whole array, then reverse the first k and the remaining n - k
    elements separately.
Tricks: Take k modulo n first, since k may be zero or exceed the length.
Edge cases:
  - k = 0
  - k larger than or equal to n
  - A single element

Time O(n), space O(1).
"""

class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums)
        k %= n  # rotating by n is a no-op, so only k mod n matters (and k may exceed n)

        def reverse(lo: int, hi: int) -> None:
            while lo < hi:
                nums[lo], nums[hi] = nums[hi], nums[lo]
                lo += 1
                hi -= 1

        # Reversing everything puts the last k elements at the front, but backwards.
        # Reversing each block separately then restores their original order.
        reverse(0, n - 1)
        reverse(0, k - 1)
        reverse(k, n - 1)
