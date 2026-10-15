"""Slow and fast pointers; when fast reaches the end, slow is at the middle.
For even length this lands on the second middle node, as the problem requires.

Time O(n), space O(1).
"""


class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow
