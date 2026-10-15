"""Two pointers with leftMax and rightMax. Water at i is
min(leftMax, rightMax) - height[i]; advance the side with the smaller max and
add that side's max minus its height.

Time O(n), space O(1).
"""


class Solution:
    def trap(self, height: List[int]) -> int:
        left, right = 0, len(height) - 1
        left_max = right_max = 0
        total = 0
        while left < right:
            if height[left] < height[right]:
                left_max = max(left_max, height[left])
                total += left_max - height[left]
                left += 1
            else:
                right_max = max(right_max, height[right])
                total += right_max - height[right]
                right -= 1
        return total
