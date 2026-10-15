"""House Robber III (#337, medium)

Approach: Post-order DFS returning the best haul with and without robbing each node,
    combined at the parent.
Tricks: Return a pair per node instead of memoising on node; skipping a node does not
    force robbing its children, so take the max of each child's pair.
Edge cases:
  - Single node
  - Skewed chain
  - Best answer skips two levels
  - Zero-valued nodes

Time O(n), space O(h).
"""

class Solution:
    def rob(self, root: Optional[TreeNode]) -> int:
        # dfs(node) returns (take, skip): the best haul from node's subtree if the node
        # itself is robbed, and if it is not. Returning both lets a parent decide without
        # revisiting children, which a plain "rob or skip" recursion would do repeatedly.
        def dfs(node):
            if node is None:
                return 0, 0
            left_take, left_skip = dfs(node.left)
            right_take, right_skip = dfs(node.right)

            # Robbing this node forces both children to be skipped.
            take = node.val + left_skip + right_skip
            # Skipping it frees each child to be either robbed or skipped, whichever is better.
            skip = max(left_take, left_skip) + max(right_take, right_skip)
            return take, skip

        return max(dfs(root))
