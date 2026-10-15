"""Reverse Nodes in k-Group (#25, hard)

Approach: Use a dummy head; for each group first check that k nodes remain, then reverse
    it in place and reconnect both ends.
Tricks: Start the reversal with prev set to the first node of the next group so the
    group's old head is already linked onward, and only reverse after confirming k nodes
    exist.
Edge cases:
  - k equals 1 or equals the length
  - Remainder shorter than k stays in order
  - Exact multiple of k
  - Single node

Time O(n), space O(1).
"""

class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        # The dummy gives the first group a predecessor to relink, because the head
        # changes whenever at least one group is reversed.
        dummy = ListNode(0, head)
        group_prev = dummy  # the node just before the current group
        while True:
            # Find the k-th node of this group. If the list ends first, the leftover
            # nodes are a short group and must stay in their original order.
            kth = group_prev
            for _ in range(k):
                kth = kth.next
                if kth is None:
                    return dummy.next
            group_next = kth.next  # first node of the following group
            # Reverse the group, but start prev at group_next instead of None so the
            # old group head ends up already pointing at the rest of the list.
            prev, curr = group_next, group_prev.next
            while curr is not group_next:
                nxt = curr.next
                curr.next = prev
                prev = curr
                curr = nxt
            # prev is now the old kth node (the new group head); the old first node
            # became the group's tail, which is where the next group's search starts.
            tail = group_prev.next
            group_prev.next = prev
            group_prev = tail
