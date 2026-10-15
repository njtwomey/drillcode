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
        dummy = ListNode(0, head)
        lead = trail = dummy
        for _ in range(n + 1):
            lead = lead.next
        while lead:
            lead = lead.next
            trail = trail.next
        trail.next = trail.next.next
        return dummy.next
