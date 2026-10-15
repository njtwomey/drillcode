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
        index = {val: i for i, val in enumerate(inorder)}
        pre = iter(preorder)

        def build(lo, hi):
            if lo > hi:
                return None
            val = next(pre)
            node = TreeNode(val)
            mid = index[val]
            node.left = build(lo, mid - 1)
            node.right = build(mid + 1, hi)
            return node

        return build(0, len(inorder) - 1)
