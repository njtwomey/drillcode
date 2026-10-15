"""Move Zeroes (#283, easy)

Approach: Write pointer for the next non-zero slot; copy non-zeros forward, then fill
    with zeros.
Tricks: Swapping instead of copying keeps it to a single pass and preserves order.
Edge cases:
  - All zeros
  - No zeros
  - Single element

Time O(n), space O(1).
"""


class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        write = 0
        for read in range(len(nums)):
            if nums[read] != 0:
                nums[write], nums[read] = nums[read], nums[write]
                write += 1
