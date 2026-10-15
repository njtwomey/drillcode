"""Reorder List (#143, medium)

Approach: Find the middle, reverse the second half, then interleave the halves.
Tricks: Cut the first half's tail to null before interleaving to avoid a cycle.
Edge cases:
  - Even and odd lengths
  - One or two nodes

Time O(n), space O(1).
"""


class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        # Zero or one node is already in order.
        if head is None or head.next is None:
            return
        # Phase 1: find the middle. Stopping when fast.next.next is null makes slow
        # the end of the first half (the longer one when the length is odd).
        slow, fast = head, head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        second = slow.next
        slow.next = None  # cut so the first half ends here
        # Phase 2: reverse the second half in place, so we can walk it from the old
        # tail. prev ends as the new head of the reversed half.
        prev = None
        while second:
            nxt = second.next  # save before overwriting the link
            second.next = prev
            prev = second
            second = nxt
        # Phase 3: weave the halves, first, last, second, second-last, ...
        # The reversed half is the same length or one shorter, so looping on it
        # alone is enough; any leftover middle node is already linked at the end.
        first, second = head, prev
        while second:
            first_next, second_next = first.next, second.next  # save both onward links
            first.next = second
            second.next = first_next
            first, second = first_next, second_next
