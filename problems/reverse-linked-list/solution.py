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
        prev = None
        curr = head
        while curr:
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node
        return prev
