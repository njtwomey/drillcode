"""Validate Binary Search Tree (#98, medium)

Approach: DFS passing an allowed (min, max) range downward, or in-order traversal
    checking strictly increasing values.
Tricks: Comparing only with the immediate parent is wrong; the bounds must come from all
    ancestors.
Edge cases:
  - Duplicates are invalid
  - Values at the integer limits, so use None or infinity as bounds

Time O(n), space O(h).
"""


class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        # Each stack entry carries the open interval (low, high) its node must fall in.
        # The bounds come from ALL ancestors, not just the parent, which is why a node
        # deep in the right subtree can still be invalid against the grandparent.
        # Iterative to avoid recursion-depth limits on skewed trees.
        stack = [(root, None, None)]
        while stack:
            node, low, high = stack.pop()
            if node is None:
                continue
            # <= and >= (not < and >) so duplicates are rejected. None means unbounded,
            # which avoids picking a sentinel that node values could equal.
            if (low is not None and node.val <= low) or (high is not None and node.val >= high):
                return False
            # Left subtree must stay below this node; right subtree must stay above it.
            # The other bound is inherited unchanged.
            stack.append((node.left, low, node.val))
            stack.append((node.right, node.val, high))
        return True
