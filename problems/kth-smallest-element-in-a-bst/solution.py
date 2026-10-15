"""Kth Smallest Element in a BST (#230, medium)

Approach: In-order traversal, stopping at the kth node.
Tricks: Iterative in-order with a stack allows an early exit.
Edge cases:
  - k = 1 (leftmost)
  - k = n (rightmost)

Time O(h + k), space O(h).
"""


class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        stack = []
        node = root
        while node or stack:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            k -= 1
            if k == 0:
                return node.val
            node = node.right
        return -1
