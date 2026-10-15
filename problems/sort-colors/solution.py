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
        # Dutch national flag. Invariants while mid <= high:
        #   nums[:low] are all 0, nums[low:mid] are all 1,
        #   nums[mid:high+1] are unexamined, nums[high+1:] are all 2.
        low, mid, high = 0, 0, len(nums) - 1
        while mid <= high:
            if nums[mid] == 0:
                # What sits at low is a known 1 (or mid itself), so after the swap
                # the value at mid is settled and both pointers advance.
                nums[low], nums[mid] = nums[mid], nums[low]
                low += 1
                mid += 1
            elif nums[mid] == 1:
                mid += 1
            else:
                # The value swapped in from high has never been looked at, so mid
                # must stay put to examine it next round.
                nums[mid], nums[high] = nums[high], nums[mid]
                high -= 1
