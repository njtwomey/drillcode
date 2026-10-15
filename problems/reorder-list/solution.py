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
        if head is None or head.next is None:
            return
        slow, fast = head, head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        second = slow.next
        slow.next = None  # cut so the first half ends here
        prev = None
        while second:
            nxt = second.next
            second.next = prev
            prev = second
            second = nxt
        first, second = head, prev
        while second:
            first_next, second_next = first.next, second.next
            first.next = second
            second.next = first_next
            first, second = first_next, second_next
