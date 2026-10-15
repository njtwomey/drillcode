"""Binary Tree Maximum Path Sum (#124, hard)

Approach: Post-order DFS returning the best downward path (node + max(0, left, right));
    update a global max with node + left + right.
Tricks: Clamp each child's contribution at 0 so negative subtrees are dropped.
Edge cases:
  - All negative values (answer is the largest single node)
  - Single node

Time O(n), space O(h).
"""


class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        best = float("-inf")

        def gain(node):
            nonlocal best
            if node is None:
                return 0
            left = max(0, gain(node.left))
            right = max(0, gain(node.right))
            best = max(best, node.val + left + right)
            return node.val + max(left, right)

        gain(root)
        return best
