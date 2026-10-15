"""Level-order traversal, recording the last node of each level.

Time O(n), space O(n).
"""
from collections import deque


class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        if root is None:
            return []
        view = []
        queue = deque([root])
        while queue:
            size = len(queue)
            for i in range(size):
                node = queue.popleft()
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

        def dfs(node, depth):
            if node is None:
                return
            if depth == len(view):
                view.append(node.val)
            dfs(node.right, depth + 1)
            dfs(node.left, depth + 1)

        dfs(root, 0)
        return view
