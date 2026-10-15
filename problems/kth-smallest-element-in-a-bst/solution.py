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
        # Iterative in-order traversal: a BST visited left, node, right yields values in
        # ascending order, so the kth node visited is the answer. The stack holds the
        # ancestors whose left subtree we are still inside, so it never exceeds height h.
        stack = []
        node = root
        while node or stack:
            # Dive as far left as possible; smaller values live down there.
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()  # next smallest unvisited value
            k -= 1
            if k == 0:  # stop early instead of walking the whole tree
                return node.val
            node = node.right  # everything bigger than node sits in its right subtree
        return -1  # unreachable when 1 <= k <= n
