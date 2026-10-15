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

# Judge notes:
# Do not return anything: modify nums in place instead.


class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        # Invariant: nums[:write] holds the non-zeros seen so far, in original order.
        # Everything between write and read is zero.
        write = 0
        for read in range(len(nums)):
            if nums[read] != 0:
                # Swap rather than copy so the skipped zeros drift to the back. When
                # write == read this swaps a slot with itself, which is harmless.
                nums[write], nums[read] = nums[read], nums[write]
                write += 1
