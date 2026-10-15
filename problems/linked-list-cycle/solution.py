"""Linked List Cycle (#141, easy)

Approach: Floyd's tortoise and hare: slow moves 1, fast moves 2, cycle if they meet.
Tricks: Check both fast and fast.next for null each step.
Edge cases:
  - Empty list
  - Single node pointing to itself
  - No cycle

Time O(n), space O(1).
"""


class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        return False
