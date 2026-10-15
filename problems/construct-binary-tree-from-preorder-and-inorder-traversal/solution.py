"""Preorder gives each subtree's root; its position in inorder splits left and right.

A value -> inorder index map avoids an O(n) search per node (values are unique).
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
