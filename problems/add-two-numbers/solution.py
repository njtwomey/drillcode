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
        # Digits are stored least significant first, so we add left to right like by hand.
        # The dummy head avoids a special case for the first node.
        dummy = tail = ListNode()
        carry = 0
        # Keep going while either list has digits OR a carry is left over (e.g. 5 + 5 = 10
        # needs an extra final node).
        while l1 or l2 or carry:
            total = carry
            if l1:
                total += l1.val
                l1 = l1.next
            if l2:
                total += l2.val
                l2 = l2.next
            # Carry is 0 or 1 (max 9 + 9 + 1 = 19).
            carry, digit = divmod(total, 10)
            tail.next = ListNode(digit)
            tail = tail.next
        return dummy.next
