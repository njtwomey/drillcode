"""Odd Even Linked List (#328, medium)

Approach: Weave the nodes into an odd chain and an even chain in one pass, then attach
    the even chain after the odd tail.
Tricks: Save the head of the even chain before relinking, and loop on even and even.next
    so the pointers never dereference null.
Edge cases:
  - Empty list and single node
  - Two nodes
  - Even and odd lengths

Time O(n), space O(1).
"""

class Solution:
    def oddEvenList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # Zero or one node is already grouped.
        if head is None or head.next is None:
            return head
        # Build two chains in place: odd positions starting at head, even positions
        # starting at head.next. Keep the even head so the chains can be joined later.
        odd, even = head, head.next
        even_head = even
        # even leads, so even and even.next both being real nodes means odd.next.next
        # exists and a full odd/even pair can be skipped over.
        while even and even.next:
            odd.next = even.next
            odd = odd.next
            even.next = odd.next
            even = even.next
        # odd is the last odd-position node; hang the even chain after it. The last
        # even node already points to null, so no cycle is created.
        odd.next = even_head
        return head
