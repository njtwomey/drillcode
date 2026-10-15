"""Construct Binary Tree from Preorder and Inorder Traversal (#105, medium)

Approach: Preorder gives the root; its position in inorder splits the left and right
    subtrees; recurse.
Tricks: A map from value to inorder index avoids an O(n) search at each node; values are
    unique.
Edge cases:
  - Single node
  - Fully left-skewed tree

Time O(n), space O(n).
"""


class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        # Value -> inorder position, so finding a root's split point is O(1), not O(n).
        index = {val: i for i, val in enumerate(inorder)}
        # Preorder is consumed strictly left to right: root, whole left subtree, whole right.
        pre = iter(preorder)

        # build(lo, hi) rebuilds the subtree whose inorder slice is inorder[lo..hi].
        def build(lo, hi):
            # Empty slice means no node here. It also ends recursion at the leaves.
            if lo > hi:
                return None
            # The next unused preorder value is this slice's root.
            val = next(pre)
            node = TreeNode(val)
            # Inorder left of mid is the left subtree, right of mid is the right subtree.
            mid = index[val]
            # Left must be built first: preorder lists the left subtree before the right,
            # and the shared iterator only works if we take values in that order.
            node.left = build(lo, mid - 1)
            node.right = build(mid + 1, hi)
            return node

        return build(0, len(inorder) - 1)
