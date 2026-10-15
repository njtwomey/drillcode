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
        # queue holds indices whose values are in decreasing order, so the front is
        # always the max of the current window. Each index is pushed and popped at
        # most once, which is why this is O(n) despite the inner while loop.
        queue = deque()
        result = []
        for i, num in enumerate(nums):
            # Anything smaller than num that is older can never be a max again (num is
            # bigger and will outlive it in the window), so discard it.
            while queue and nums[queue[-1]] <= num:
                queue.pop()
            queue.append(i)
            # Only the front can be out of range, since indices are in increasing order.
            if queue[0] <= i - k:
                queue.popleft()
            # Start reporting once the first full window of k elements exists.
            if i >= k - 1:
                result.append(nums[queue[0]])
        return result
