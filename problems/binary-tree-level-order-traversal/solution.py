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
        if root is None:
            return []
        levels = []
        queue = deque([root])
        while queue:
            level = []
            for _ in range(len(queue)):
                node = queue.popleft()
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            levels.append(level)
        return levels
