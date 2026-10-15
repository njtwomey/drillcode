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
        low, mid, high = 0, 0, len(nums) - 1
        while mid <= high:
            if nums[mid] == 0:
                nums[low], nums[mid] = nums[mid], nums[low]
                low += 1
                mid += 1
            elif nums[mid] == 1:
                mid += 1
            else:
                nums[mid], nums[high] = nums[high], nums[mid]
                high -= 1
