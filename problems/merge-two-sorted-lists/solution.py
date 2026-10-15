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
        dummy = tail = ListNode()
        while list1 and list2:
            if list1.val <= list2.val:
                tail.next = list1
                list1 = list1.next
            else:
                tail.next = list2
                list2 = list2.next
            tail = tail.next
        tail.next = list1 or list2
        return dummy.next
