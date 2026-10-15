"""Binary Tree Right Side View (#199, medium)

Approach: Level-order traversal, recording the last node of each level.
Tricks: DFS visiting right before left and recording the first node seen at each depth
    also works.
Edge cases:
  - Left subtree deeper than the right, so left nodes appear in the view

Time O(n), space O(n).
"""
from collections import deque


class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        if root is None:
            return []
        view = []
        # Level-order BFS; the last node of each level is the one visible from the right.
        queue = deque([root])
        while queue:
            size = len(queue)
            for i in range(size):
                node = queue.popleft()
                # Last in this level = rightmost.
                if i == size - 1:
                    view.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
        return view

    # DFS alternative: visit right before left, keep the first node seen at each depth.
    def rightSideViewDFS(self, root: Optional[TreeNode]) -> List[int]:
        view = []

        # Right-first order means the first node reaching a new depth is the rightmost.
        def dfs(node, depth):
            if node is None:
                return
            # view has one entry per depth seen so far; equal length means a new depth.
            if depth == len(view):
                view.append(node.val)
            dfs(node.right, depth + 1)
            dfs(node.left, depth + 1)

        dfs(root, 0)
        return view
