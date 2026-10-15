"""Find the Duplicate Number (#287, medium)

Approach: Treat each value as a next pointer; Floyd's cycle detection finds the cycle
    entrance.
Tricks: The duplicate is the entrance, not the meeting point; phase two restarts one
    pointer at index 0.
Edge cases:
  - Duplicate appearing more than twice
  - Duplicate at index 0

Time O(n), space O(1).
"""


class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        slow = fast = nums[0]
        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break
        slow = nums[0]
        while slow != fast:
            slow = nums[slow]
            fast = nums[fast]
        return slow
