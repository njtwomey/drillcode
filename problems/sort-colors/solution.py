"""Sort Colors (#75, medium)

Approach: Dutch national flag: low, mid, high pointers; swap 0s to low and 2s to high.
Tricks: Do not advance mid after a swap with high, since the swapped-in value is
    unexamined.
Edge cases:
  - Already sorted
  - Single colour
  - Two elements

Time O(n), space O(1).
"""


class Solution:
    def sortColors(self, nums: List[int]) -> None:
        # Dutch national flag. Invariants while mid <= hi:
        #   nums[:lo] are all 0, nums[lo:mid] are all 1,
        #   nums[mid:hi+1] are unexamined, nums[hi+1:] are all 2.
        lo, mid, hi = 0, 0, len(nums) - 1
        while mid <= hi:
            if nums[mid] == 0:
                # What sits at lo is a known 1 (or mid itself), so after the swap
                # the value at mid is settled and both pointers advance.
                nums[lo], nums[mid] = nums[mid], nums[lo]
                lo += 1
                mid += 1
            elif nums[mid] == 1:
                mid += 1
            else:
                # The value swapped in from hi has never been looked at, so mid
                # must stay put to examine it next round.
                nums[mid], nums[hi] = nums[hi], nums[mid]
                hi -= 1
