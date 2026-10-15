"""Binary Tree Level Order Traversal (#102, medium)

Approach: BFS with a queue, taking a snapshot of the queue length at the start of each
    level.
Tricks: Reading len(queue) before the inner loop separates levels without sentinels.
Edge cases:
  - Empty tree
  - Single node

Time O(n), space O(n).
"""
from collections import deque


class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        # Guard: deque([None]) would crash on node.val.
        if root is None:
            return []
        result = []
        # BFS queue holds the nodes of the current level, then the next one.
        queue = deque([root])
        while queue:
            level = []
            # len(queue) is frozen at the level's size, so children appended inside
            # the loop wait for the next pass. Every node is handled once: O(n).
            for _ in range(len(queue)):
                node = queue.popleft()
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            result.append(level)
        return result
