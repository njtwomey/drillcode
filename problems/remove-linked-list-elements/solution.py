"""Remove Linked List Elements (#203, easy)

Approach: Walk with a dummy head, bypassing any next node whose value matches and
    advancing only when it does not.
Tricks: Do not advance prev after a deletion, since the new next node may match too; the
    dummy handles a removed head.
Edge cases:
  - Empty list
  - Head or entire list matches
  - Consecutive matches
  - No match

Time O(n), space O(1).
"""

class Solution:
    def removeElements(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:
        # The dummy means a matching head needs no special case: it is just another
        # node that follows prev.
        dummy = ListNode(0, head)
        prev = dummy
        while prev.next:
            if prev.next.val == val:
                # Bypass the node but keep prev put: the new next node may match too.
                prev.next = prev.next.next
            else:
                prev = prev.next
        return dummy.next
