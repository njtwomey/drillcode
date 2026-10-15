"""Maximum Depth of Binary Tree (#104, easy)

Approach: 1 + max(depth(left), depth(right)).
Edge cases:
  - Empty tree is depth 0

Time O(n), space O(h).
"""


class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:  # Base case: an empty tree has no levels.
            return 0
        # This node adds one level on top of the deeper of its two subtrees.
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
