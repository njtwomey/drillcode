"""Convert Sorted Array to Binary Search Tree (#108, easy)

Approach: Recursively pick the middle element of each index range as the root, building
    the two halves as subtrees.
Tricks: Recurse on index bounds rather than slicing to stay O(n); the middle root keeps
    subtree sizes within one so the tree is balanced.
Edge cases:
  - Single value
  - Even length (two valid middles)
  - Two values

Time O(n), space O(log n).
"""

class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        # build(lo, hi) makes a tree from nums[lo..hi]. Using indices avoids copying slices.
        def build(lo, hi):
            if lo > hi:
                return None
            # The middle element as root puts about half the values on each side, and
            # every value left of it is smaller (sorted input), so the BST property
            # holds and the two subtree sizes differ by at most one: height balanced.
            mid = (lo + hi) // 2
            node = TreeNode(nums[mid])
            node.left = build(lo, mid - 1)
            node.right = build(mid + 1, hi)
            return node

        return build(0, len(nums) - 1)
