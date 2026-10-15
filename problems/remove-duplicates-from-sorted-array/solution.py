"""Remove Duplicates from Sorted Array (#26, easy)

Approach: Read and write pointers; copy a value forward only when it differs from the
    last value kept.
Tricks: Because the array is sorted, comparing with the last kept element (nums[write -
    1]) is enough, and the return value is the write index.
Edge cases:
  - Single element
  - All elements equal
  - No duplicates at all

Time O(n), space O(1).
"""

class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        # write is the length of the unique prefix built so far, and the slot where the
        # next new value goes. nums[0] is unique by definition, so scanning starts at 1.
        write = 1
        for read in range(1, len(nums)):
            # The array is sorted, so any new value differs from the last kept one;
            # equal values are exactly the duplicates and are skipped.
            if nums[read] != nums[write - 1]:
                nums[write] = nums[read]
                write += 1
        return write
