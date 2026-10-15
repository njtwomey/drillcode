"""Binary Tree Cameras (#968, hard)

Approach: Post-order DFS with three node states (needs cover, covered, has camera),
    placing a camera on the parent of any uncovered child.
Tricks: Never put a camera on a leaf; wait and place it on its parent, then give the
    root its own camera if it still needs cover.
Edge cases:
  - Single node needs one camera
  - Root left uncovered after the DFS
  - Long skewed chain (one camera per three nodes)
  - Perfect binary tree

Time O(n), space O(h).
"""

class Solution:
    def minCameraCover(self, root: Optional[TreeNode]) -> int:
        NEEDS, COVERED, CAMERA = 0, 1, 2
        cameras = 0

        # dfs(node) reports the state of node after its subtree is handled:
        #   NEEDS: not watched yet, the parent must cover it
        #   COVERED: watched by a child's camera, holds none itself
        #   CAMERA: has a camera
        # Placing cameras as high as possible (on the parent of an unwatched node, never
        # on the node itself) is optimal, because a camera there also watches the grandparent.
        def dfs(node):
            nonlocal cameras
            if node is None:
                return COVERED  # nothing to watch, and nothing to force a camera above
            left = dfs(node.left)
            right = dfs(node.right)
            if left == NEEDS or right == NEEDS:
                cameras += 1
                return CAMERA
            if left == CAMERA or right == CAMERA:
                return COVERED
            return NEEDS

        # The root has no parent, so if it still needs cover it gets its own camera.
        if dfs(root) == NEEDS:
            cameras += 1
        return cameras
