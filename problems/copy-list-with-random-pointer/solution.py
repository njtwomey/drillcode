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
        copies = {None: None}
        node = head
        while node:
            copies[node] = Node(node.val)
            node = node.next
        node = head
        while node:
            copies[node].next = copies[node.next]
            copies[node].random = copies[node.random]
            node = node.next
        return copies[head]
