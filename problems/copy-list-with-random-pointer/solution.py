"""Copy List with Random Pointer (#138, medium)

Approach: First pass maps each node to its copy; second pass wires next and random
    through the map.
Tricks: The O(1) space version interleaves copies after originals, then splits them
    apart.
Edge cases:
  - Random pointing to itself
  - Random null
  - Empty list

Time O(n), space O(n).
"""


class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        # Old node -> new node. None maps to None so null next/random need no special case.
        copies = {None: None}
        # Pass 1: create every copy first, so pass 2 can point at nodes that come later
        # (random can point forward or backward).
        node = head
        while node:
            copies[node] = Node(node.val)
            node = node.next
        # Pass 2: wire pointers by translating each original target through the map.
        node = head
        while node:
            copies[node].next = copies[node.next]
            copies[node].random = copies[node.random]
            node = node.next
        return copies[head]
