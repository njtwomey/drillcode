"""Two passes with a map: first create a copy of each node, then wire next and random through the map.

Time O(n), space O(n). (The O(1)-space trick interleaves copies after originals, then splits them.)
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
