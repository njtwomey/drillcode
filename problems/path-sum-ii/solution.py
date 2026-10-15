"""Path Sum II (#113, medium)

Approach: DFS with one shared path list, pushing on entry and popping on exit, copying
    it at each matching leaf.
Tricks: Append a copy of the path, not the list itself, and pop on every exit so
    siblings start from the right prefix.
Edge cases:
  - Empty tree
  - Matching sum at a non-leaf must not be recorded
  - Negative and zero values
  - Several matching paths

Time O(n²), space O(h).
"""

class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        result = []
        path = []

        # path holds the values from the root to the node being visited. Each call pushes
        # its value and pops it again on the way out, so siblings reuse the same list.
        def dfs(node, remaining):
            if node is None:
                return
            path.append(node.val)
            remaining -= node.val
            if node.left is None and node.right is None and remaining == 0:
                # Copy: path keeps changing after this call returns.
                result.append(path[:])
            else:
                dfs(node.left, remaining)
                dfs(node.right, remaining)
            path.pop()

        dfs(root, targetSum)
        return result
