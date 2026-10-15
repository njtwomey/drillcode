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
        # copies maps original -> clone. It doubles as the visited set, which stops
        # infinite loops on cycles and makes sure each node is cloned once.
        copies = {node: Node(node.val)}
        queue = deque([node])
        while queue:
            curr = queue.popleft()
            for neighbour in curr.neighbors:
                # First sighting: create the clone now so the edge below can point at it
                # before the neighbour itself is processed.
                if neighbour not in copies:
                    copies[neighbour] = Node(neighbour.val)
                    queue.append(neighbour)
                # Every edge is added from its source side, so each is copied exactly once.
                copies[curr].neighbors.append(copies[neighbour])
        return copies[node]
