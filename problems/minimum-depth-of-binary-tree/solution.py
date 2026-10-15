"""Minimum Depth of Binary Tree (#111, easy)

Approach: BFS by level, returning the depth of the first leaf found.
Tricks: A node with one child is not a leaf, so min(left, right) with an empty side
    returning 0 gives the wrong answer; BFS sidesteps this and exits early.
Edge cases:
  - Empty tree is 0
  - Single node is 1
  - Skewed chain, where only one side has a leaf

Time O(n), space O(n).
"""

class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0

        # Level-order search: the first leaf met is the nearest one, so we can stop
        # there instead of walking the whole tree like a depth-first search would.
        level = [root]
        depth = 1
        while level:
            nxt = []
            for node in level:
                if node.left is None and node.right is None:
                    return depth
                # A node with one child is not a leaf, so only that child is followed.
                if node.left:
                    nxt.append(node.left)
                if node.right:
                    nxt.append(node.right)
            level = nxt
            depth += 1
        return depth  # unreachable: every finite tree has a leaf
