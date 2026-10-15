"""First Missing Positive (#41, hard)

Approach: Cyclic placement; swap each value v in 1..n into index v - 1, then the first
    index holding the wrong value gives the answer.
Tricks: The answer lies in 1..n+1, and the swap loop must stop when the target slot
    already holds the value, or duplicates spin forever.
Edge cases:
  - All values out of range (negatives, zeros, above n)
  - Duplicates
  - Permutation of 1..n (answer n + 1)

Time O(n), space O(1).
"""

class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        n = len(nums)
        # The answer is in 1..n+1: n slots can hold at most 1..n, and if they all do the
        # answer is n+1. So treat the array itself as a table where value v belongs at
        # index v - 1, ignoring everything outside 1..n (negatives, zeros, huge values).
        for i in range(n):
            # Keep swapping until slot i holds a value that is out of range or already
            # sitting in its home slot. The second test also stops the loop on duplicates,
            # which would otherwise swap with themselves forever.
            while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
                j = nums[i] - 1  # compute first: assigning nums[i] would change the target
                nums[i], nums[j] = nums[j], nums[i]
        # Each placed value costs at most one swap, so the loops are O(n) in total.
        # The first slot not holding index + 1 names the smallest missing positive.
        for i in range(n):
            if nums[i] != i + 1:
                return i + 1
        return n + 1
