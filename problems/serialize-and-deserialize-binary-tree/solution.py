"""Pre-order traversal with explicit "#" null markers, comma-delimited so
negative and multi-digit values survive. Deserialise by consuming tokens in the
same order with an iterator.

Time O(n), space O(n).
"""


class Codec:
    def serialize(self, root):
        """Encodes a tree to a single string."""
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
        return ",".join(out)

    def deserialize(self, data):
        """Decodes your encoded data to tree."""
        tokens = iter(data.split(","))

        def build():
            token = next(tokens)
            if token == "#":
                return None
            node = TreeNode(int(token))
            node.left = build()
            node.right = build()
            return node

        return build()
