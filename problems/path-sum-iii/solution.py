"""Path Sum III (#437, medium)

Approach: DFS with a running prefix sum and a hash map of prefix-sum counts along the
    current root path.
Tricks: Seed the map with {0: 1} for paths starting at the root, and decrement the entry
    on exit so sibling subtrees do not see each other.
Edge cases:
  - Empty tree
  - Negative values and zeros
  - Paths that start below the root
  - Large values

Time O(n), space O(h).
"""

class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:
        # seen[s] is how many nodes on the current root-to-node path have prefix sum s,
        # counting the empty prefix (sum 0). A downward path ending here sums to the
        # target exactly when it starts just below an ancestor whose prefix is
        # (current prefix - target).
        seen = {0: 1}

        def dfs(node, prefix):
            if node is None:
                return 0
            prefix += node.val
            count = seen.get(prefix - targetSum, 0)

            seen[prefix] = seen.get(prefix, 0) + 1
            count += dfs(node.left, prefix) + dfs(node.right, prefix)
            # Leaving this node: remove it so the sibling subtree only sees its own ancestors.
            seen[prefix] -= 1
            return count

        return dfs(root, 0)
