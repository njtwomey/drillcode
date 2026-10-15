"""Recursive: reverse the rest of the list, then point the next node back at head.

Time O(n), space O(n) for the call stack.
"""


class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # Base case: empty list or the last node is already its own reversal.
        if head is None or head.next is None:
            return head
        # Trust the recursion: afterwards head.next is the tail of the reversed rest,
        # and new_head is the old last node, which stays the head all the way up.
        new_head = self.reverseList(head.next)
        head.next.next = head  # make the following node point back at us
        head.next = None  # cut the old forward link so the new tail ends the list, no cycle
        return new_head
