"""Clone Graph (#133, medium)

Approach: DFS or BFS with a map from original node to its copy.
Tricks: Insert the copy in the map before recursing into neighbours, or cycles recurse
    forever.
Edge cases:
  - Null input
  - Single node with no neighbours

Time O(V + E), space O(V).
"""
from collections import deque


class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        if node is None:
            return None
        copies = {node: Node(node.val)}
        queue = deque([node])
        while queue:
            current = queue.popleft()
            for neighbour in current.neighbors:
                if neighbour not in copies:
                    copies[neighbour] = Node(neighbour.val)
                    queue.append(neighbour)
                copies[current].neighbors.append(copies[neighbour])
        return copies[node]
