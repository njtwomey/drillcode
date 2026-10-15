"""Next Greater Element II (#503, medium)

Approach: Decreasing stack of indices over two passes (i from 0 to 2n - 1, value nums[i
    % n]), resolving waiting indices when a larger value arrives.
Tricks: Iterate 2n times to simulate the circle but push indices only on the first pass.
Edge cases:
  - Maximum element (and its duplicates) gets -1
  - All elements equal
  - Answer found only by wrapping around
  - Single element

Time O(n), space O(n).
"""

class Solution:
    def nextGreaterElements(self, nums: List[int]) -> List[int]:
        n = len(nums)
        result = [-1] * n
        # The stack holds indices still waiting for a greater value; their values are
        # non-increasing from bottom to top. Going around the circle is simulated by
        # making two passes over the array (index i % n).
        stack = []
        for i in range(2 * n):
            value = nums[i % n]
            while stack and nums[stack[-1]] < value:
                result[stack.pop()] = value
            # Only the first pass registers indices as waiting; the second pass just
            # resolves the leftovers, and pushing again would duplicate work.
            if i < n:
                stack.append(i)
        return result
