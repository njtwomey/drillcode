"""Merge Two Sorted Lists (#21, easy)

Approach: Dummy head; take the smaller node each step, then append whatever remains.
Tricks: The dummy head removes the special case for the first node.
Edge cases:
  - One list empty
  - Both empty
  - One list entirely smaller than the other

Time O(m + n), space O(1).
"""


class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        # dummy is a placeholder before the real head; tail is where the next node attaches.
        dummy = tail = ListNode()
        # Each list is sorted, so the smaller front node is the next smallest overall.
        while list1 and list2:
            if list1.val <= list2.val:  # <= keeps the merge stable for equal values.
                tail.next = list1
                list1 = list1.next
            else:
                tail.next = list2
                list2 = list2.next
            tail = tail.next
        # At most one list has nodes left, and it is already sorted and larger than all
        # merged nodes, so link the whole remainder in O(1).
        tail.next = list1 or list2
        return dummy.next  # Skip the placeholder.
