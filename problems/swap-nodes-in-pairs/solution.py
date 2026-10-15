"""Swap Nodes in Pairs (#24, medium)

Approach: Walk with a dummy head and a pointer to the node before each pair, rewiring
    the pair's three links in place.
Tricks: Rewire in the order first.next, second.next, prev.next so no link is lost, then
    advance prev to the old first node.
Edge cases:
  - Empty list and single node
  - Odd length leaves the last node alone
  - Two nodes

Time O(n), space O(1).
"""

class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # The dummy lets the first pair be swapped like any other, since the head
        # itself changes when the list has at least two nodes.
        dummy = ListNode(0, head)
        prev = dummy  # always the node just before the pair being swapped
        while prev.next and prev.next.next:
            first = prev.next
            second = first.next
            # Rewire prev -> second -> first -> (rest). Order matters: first must take
            # over second's tail before second is pointed back at first.
            first.next = second.next
            second.next = first
            prev.next = second
            # first is now the tail of the swapped pair, so it precedes the next pair.
            prev = first
        return dummy.next
