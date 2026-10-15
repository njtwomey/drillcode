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
        # Two different quantities are in play:
        #  - best: the best path that bends at some node (uses both children).
        #  - gain() return value: the best path that goes only DOWN from a node, since
        #    a parent can extend just one branch.
        best = float("-inf")  # -inf (not 0) so all-negative trees are handled

        def gain(node):
            nonlocal best
            if node is None:
                return 0
            # A negative branch only hurts, so treat it as "don't take it" (0).
            left = max(0, gain(node.left))
            right = max(0, gain(node.right))
            # Candidate answer: this node is the top of the path, joining both sides.
            best = max(best, node.val + left + right)
            # Report upward only one side; a path can't fork when it continues up.
            return node.val + max(left, right)

        gain(root)
        return best
