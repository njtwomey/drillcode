"""Max Consecutive Ones III (#1004, medium)

Approach: Longest window containing at most k zeros; grow right, and shrink left
    whenever the zero count exceeds k.
Tricks: Never flip anything, just count zeros in the window; k = 0 degenerates to the
    longest run of ones.
Edge cases:
  - k = 0
  - k larger than the number of zeros
  - All zeros or all ones

Time O(n), space O(1).
"""

class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        # Longest window containing at most k zeros: those zeros are the ones we flip.
        left = 0
        zeros = 0
        best = 0
        for right, num in enumerate(nums):
            if num == 0:
                zeros += 1
            # Over budget: advance left until a zero leaves the window. A plain while
            # keeps the invariant zeros <= k true before we measure.
            while zeros > k:
                if nums[left] == 0:
                    zeros -= 1
                left += 1
            best = max(best, right - left + 1)
        return best
