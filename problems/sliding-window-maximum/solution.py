"""Sliding Window Maximum (#239, hard)

Approach: Deque of indices with decreasing values; pop smaller values from the back on
    push, drop the front once it leaves the window.
Tricks: Store indices so expiry is a position check.
Edge cases:
  - k = 1 (output equals input)
  - k = n
  - All values equal

Time O(n), space O(k).
"""
from collections import deque


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        window = deque()
        result = []
        for i, num in enumerate(nums):
            while window and nums[window[-1]] <= num:
                window.pop()
            window.append(i)
            if window[0] <= i - k:
                window.popleft()
            if i >= k - 1:
                result.append(nums[window[0]])
        return result
