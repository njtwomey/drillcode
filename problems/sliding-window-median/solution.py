"""Sliding Window Median (#480, hard)

Approach: Maintain the window in a sorted list, using bisect to remove the outgoing
    value and insort to add the incoming one.
Tricks: Average the two middle values with true division for even k; two heaps with lazy
    deletion also work but are fiddly.
Edge cases:
  - k = 1
  - k equals the array length
  - Values near the 32-bit limits
  - Even window sizes give .5 medians

Time O(n * k), space O(k).
"""

from bisect import bisect_left, insort


class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        # Keep the current window as a sorted list. insort and a bisect-then-delete
        # cost O(log k) to find the spot plus a fast memmove to shift elements, which is
        # far simpler than juggling two heaps with lazy deletion.
        window = sorted(nums[:k])
        mid = k // 2
        result = []
        for i in range(k, len(nums) + 1):
            if k % 2:
                result.append(window[mid])
            else:
                # Even size: average the two middle values (true division, not //).
                result.append((window[mid - 1] + window[mid]) / 2)
            if i == len(nums):
                break
            # Slide: drop the element leaving on the left, add the new one on the right.
            del window[bisect_left(window, nums[i - k])]
            insort(window, nums[i])
        return result
