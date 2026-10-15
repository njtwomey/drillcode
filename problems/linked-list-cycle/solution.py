"""Floyd's tortoise and hare: slow moves one step, fast moves two; they meet iff there is a cycle.

Check both fast and fast.next for None each step.
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
