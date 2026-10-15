"""Reverse Linked List (#206, easy)

Approach: Iterate with prev and curr, saving next before re-pointing each node backwards.
Tricks: Save next before overwriting curr.next; the recursive version is a common
    follow-up.
Edge cases:
  - Empty list
  - Single node

Time O(n), space O(1).
"""


class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # Invariant: prev heads the already-reversed part, curr heads the untouched rest.
        prev = None
        curr = head
        while curr:
            nxt = curr.next  # save it, or re-pointing below loses the rest
            curr.next = prev
            # Advance both pointers one step. When curr runs off the end, prev is the
            # old tail, i.e. the new head.
            prev = curr
            curr = nxt
        return prev
