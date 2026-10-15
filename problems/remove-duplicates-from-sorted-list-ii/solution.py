"""Remove Duplicates from Sorted List II (#82, medium)

Approach: Walk with a dummy head and a trailing prev pointer; skip whole runs of equal
    values and relink prev past them.
Tricks: Do not advance prev when a run is removed, because the next run may also be a
    duplicate; the dummy covers a duplicated head.
Edge cases:
  - Duplicated head value
  - All values equal gives an empty list
  - Duplicates at the tail
  - Empty list

Time O(n), space O(1).
"""

class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # The dummy handles the case where the original head is itself a duplicate
        # and has to be removed.
        dummy = ListNode(0, head)
        prev = dummy  # last node known to be kept; its next is the candidate
        curr = head
        while curr:
            # Skip to the last node of this run of equal values.
            if curr.next and curr.next.val == curr.val:
                while curr.next and curr.next.val == curr.val:
                    curr = curr.next
                # The whole run is dropped. prev stays put because the node after the
                # run might start another duplicate run that must also be dropped.
                prev.next = curr.next
            else:
                prev = curr  # unique value: keep it and move the anchor forward
            curr = curr.next
        return dummy.next
