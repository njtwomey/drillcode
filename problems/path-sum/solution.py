"""Path Sum (#112, easy)

Approach: DFS carrying the remaining target down, checking it is zero at a leaf.
Tricks: Only a node with no children ends a path, so a missing child must return false
    rather than test the remainder.
Edge cases:
  - Empty tree is false even for target 0
  - Node with one child is not a leaf
  - Negative values

Time O(n), space O(h).
"""

class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        # An empty tree has no root-to-leaf path. This is also the base case for a missing
        # child, and it must not count as a leaf, or [1, 2] would wrongly match target 1.
        if root is None:
            return False

        # Carry the remainder down instead of summing a whole path at each leaf.
        remaining = targetSum - root.val

        # Only a real leaf (no children at all) can end a path.
        if root.left is None and root.right is None:
            return remaining == 0

        return self.hasPathSum(root.left, remaining) or self.hasPathSum(root.right, remaining)
