"""Same Tree (#100, easy)

Approach: Both null → true; one null → false; compare values then recurse on both sides.
Edge cases:
  - Both empty
  - Same shape with different values
  - Same values with different shape

Time O(n), space O(h).
"""


class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if p is None and q is None:
            return True
        if p is None or q is None or p.val != q.val:
            return False
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
