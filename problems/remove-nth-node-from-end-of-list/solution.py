"""Remove Nth Node From End of List (#19, medium)

Approach: Two pointers n + 1 apart from a dummy head; when the lead reaches the end, the
    trailer is before the target.
Tricks: The dummy head handles removal of the first node.
Edge cases:
  - n equals the list length (remove the head)
  - Single node

Time O(n), space O(1).
"""


class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        # The dummy gives the head a predecessor, so removing the first node needs
        # no special case.
        dummy = ListNode(0, head)
        fast = slow = dummy
        # Open a gap of n + 1 nodes between the pointers. The extra 1 means that when
        # fast falls off the end, slow sits just BEFORE the node to delete.
        for _ in range(n + 1):
            fast = fast.next
        # Move both in lockstep; the gap stays fixed, so one pass finds the spot
        # without needing the list length.
        while fast:
            fast = fast.next
            slow = slow.next
        slow.next = slow.next.next  # unlink the target
        return dummy.next  # not head: head itself may have been removed
