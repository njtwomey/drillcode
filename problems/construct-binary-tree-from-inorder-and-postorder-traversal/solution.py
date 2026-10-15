"""Construct Binary Tree from Inorder and Postorder Traversal (#106, medium)

Approach: Take roots from the end of postorder (right subtree first) and split the
    inorder range using a value-to-index map.
Tricks: Reading postorder backwards gives root, right, left, so build the right subtree
    before the left one; a hash map avoids rescanning inorder.
Edge cases:
  - Single node
  - Fully left or fully right skewed tree
  - Negative values

Time O(n), space O(n).
"""

class Solution:
    def buildTree(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
        # Values are unique, so a value pins down its position in the inorder list.
        index = {val: i for i, val in enumerate(inorder)}

        # Postorder is left, right, root. Read backwards it is root, right, left, so each
        # next value is the root of the subtree we are about to build, right side first.
        post = iter(reversed(postorder))

        # build(lo, hi) rebuilds the subtree whose inorder slice is inorder[lo..hi].
        def build(lo, hi):
            # An empty slice is a missing child, and the base case for every leaf.
            if lo > hi:
                return None
            val = next(post)
            node = TreeNode(val)
            mid = index[val]
            # Right must be built before left: the reversed postorder lists the whole
            # right subtree first, and the shared iterator only works in that order.
            node.right = build(mid + 1, hi)
            node.left = build(lo, mid - 1)
            return node

        return build(0, len(inorder) - 1)
