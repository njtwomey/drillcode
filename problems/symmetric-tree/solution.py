"""Symmetric Tree (#101, easy)

Approach: Recursively compare two subtrees, pairing the left child of one with the right
    child of the other.
Tricks: Compare outer with outer and inner with inner; checking each level's values for
    a palindrome misses shape differences.
Edge cases:
  - Single node
  - Only one child present
  - Same shape but values or positions not mirrored

Time O(n), space O(h).
"""

class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        # mirror(a, b) asks whether subtree a is the left-right reflection of subtree b.
        def mirror(a, b):
            if a is None and b is None:
                return True
            # Exactly one side missing, or different values: the shapes cannot match.
            if a is None or b is None or a.val != b.val:
                return False
            # Reflection pairs outer children together and inner children together.
            return mirror(a.left, b.right) and mirror(a.right, b.left)

        return mirror(root.left, root.right) if root else True
