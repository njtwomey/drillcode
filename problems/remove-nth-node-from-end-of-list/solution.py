"""Two pointers from a dummy head: advance the lead n + 1 steps, then move both
until the lead falls off the end; the trailer is just before the target.

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
