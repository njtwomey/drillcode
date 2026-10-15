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
        # Both ran out together: identical so far.
        if p is None and q is None:
            return True
        # Exactly one is missing (shape differs) or values differ. The None checks come
        # first so p.val is never read on None.
        if p is None or q is None or p.val != q.val:
            return False
        # Both subtrees must match; `and` stops at the first mismatch.
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
