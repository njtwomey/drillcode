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
        # window holds indices whose values are in decreasing order, so the front is
        # always the max of the current window. Each index is pushed and popped at
        # most once, which is why this is O(n) despite the inner while loop.
        window = deque()
        result = []
        for i, num in enumerate(nums):
            # Anything smaller than num that is older can never be a max again (num is
            # bigger and will outlive it in the window), so discard it.
            while window and nums[window[-1]] <= num:
                window.pop()
            window.append(i)
            # Only the front can be out of range, since indices are in increasing order.
            if window[0] <= i - k:
                window.popleft()
            # Start reporting once the first full window of k elements exists.
            if i >= k - 1:
                result.append(nums[window[0]])
        return result
