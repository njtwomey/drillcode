"""Reverse Linked List II (#92, medium)

Approach: Walk to the node before position left, then repeatedly move the node after the
    segment's first node to the front of the segment.
Tricks: A dummy head handles left equal to 1, and the first segment node never moves so
    it naturally becomes the segment tail already linked to the rest.
Edge cases:
  - left equals 1 (head changes)
  - right equals the length
  - left equals right
  - Single node

Time O(n), space O(1).
"""

class Solution:
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        # The dummy covers left == 1, where the head itself moves.
        dummy = ListNode(0, head)
        # Walk to the node just before position left; it stays fixed and anchors the
        # reversed segment.
        before = dummy
        for _ in range(left - 1):
            before = before.next
        # curr is the first node of the segment and will end up as its tail. Instead
        # of flipping every link, repeatedly pull the node after curr to the front of
        # the segment: this reverses it in a single pass with no extra pointers kept.
        curr = before.next
        for _ in range(right - left):
            nxt = curr.next
            curr.next = nxt.next    # unlink nxt from behind curr
            nxt.next = before.next  # put it ahead of the current segment head
            before.next = nxt
        return dummy.next
