"""Recursive: reverse the rest of the list, then point the next node back at head.

Time O(n), space O(n) for the call stack.
"""


class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        new_head = self.reverseList(head.next)
        head.next.next = head
        head.next = None
        return new_head
