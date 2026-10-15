"""Middle of the Linked List (#876, easy)

Approach: Slow and fast pointers; slow is at the middle when fast reaches the end.
Tricks: For even length this gives the second middle, which is what the problem wants.
Edge cases:
  - Single node
  - Two nodes

Time O(n), space O(1).
"""


class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # Fast moves twice as quickly, so when it runs off the end slow is halfway.
        slow = fast = head
        # Odd length: fast stops on the last node. Even length: fast becomes None, which
        # leaves slow on the second of the two middles, as required.
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow
