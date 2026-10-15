"""Add Two Numbers (#2, medium)

Approach: Walk both lists with a carry, building the result from a dummy head.
Tricks: Loop while either list or the carry is non-zero.
Edge cases:
  - Different lengths
  - Final carry producing an extra node (e.g. 5 + 5)

Time O(max(m, n)), space O(1).
"""


class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = tail = ListNode()
        carry = 0
        while l1 or l2 or carry:
            total = carry
            if l1:
                total += l1.val
                l1 = l1.next
            if l2:
                total += l2.val
                l2 = l2.next
            carry, digit = divmod(total, 10)
            tail.next = ListNode(digit)
            tail = tail.next
        return dummy.next
