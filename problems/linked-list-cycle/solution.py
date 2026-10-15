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
        # Fast gains one node on slow per step. Inside a cycle the gap shrinks by 1 each
        # step, so fast must land exactly on slow. Without a cycle fast hits the end.
        slow = fast = head
        while fast and fast.next:  # Both checks keep fast.next.next from hitting None.
            slow = slow.next
            fast = fast.next.next
            if slow is fast:  # Compare identity, not values: values can repeat.
                return True
        return False
