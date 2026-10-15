"""Serialize and Deserialize Binary Tree (#297, hard)

Approach: Pre-order with explicit null markers; deserialise by consuming tokens in the
    same order.
Tricks: Null markers make pre-order alone sufficient; level-order works too.
Edge cases:
  - Empty tree
  - Negative and multi-digit values (delimit tokens)
  - Single node

Time O(n), space O(n).
"""


class Codec:
    def serialize(self, root):
        """Encodes a tree to a single string."""
        # Pre-order (node, left, right) with "#" for null. Recording the nulls is what
        # makes the shape unambiguous from one traversal. Iterative to avoid deep
        # recursion; push right first so left is popped (visited) first.
        out = []
        stack = [root]
        while stack:
            node = stack.pop()
            if node is None:
                out.append("#")
            else:
                out.append(str(node.val))
                stack.append(node.right)
                stack.append(node.left)
        # Commas delimit tokens so multi-digit and negative values stay intact.
        return ",".join(out)

    def deserialize(self, data):
        """Decodes your encoded data to tree."""
        # A shared iterator is the "cursor": each build() call consumes exactly the
        # tokens of its own subtree, leaving the rest for the caller.
        tokens = iter(data.split(","))

        def build():
            token = next(tokens)
            if token == "#":
                return None  # null marker ends this branch
            node = TreeNode(int(token))
            # Same order as serialize: left subtree fully, then right.
            node.left = build()
            node.right = build()
            return node

        return build()
