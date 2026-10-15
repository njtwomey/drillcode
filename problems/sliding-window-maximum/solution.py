"""Monotonic deque of indices whose values decrease. On each push, pop smaller
values from the back; drop the front once its index leaves the window. The
front is always the window maximum.

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
