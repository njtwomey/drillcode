---
title: Serialise, rebuild, compare
area: Trees
topics: [Tree, Design]
problems:
  - serialize-and-deserialize-binary-tree
  - construct-binary-tree-from-preorder-and-inorder-traversal
related: [tree-recursion-return-and-best, bst-invariant]
---
## Reach for it when

- The statement says "serialize" and "deserialize", or "encode a tree as a string".
- A tree must be rebuilt from traversal output (preorder with inorder).
- You need to compare subtrees by a fingerprint instead of walking both.

## Setup

- Serialise: `result = []` of tokens and a `stack = [root]` for an iterative pre-order. Push the right child first so the left is popped first. Append `"#"` for a null.
- Deserialise: `tokens = iter(data.split(","))`, a shared iterator, and an inner `def build()` that takes the next token. The iterator is the cursor, so there is no index to maintain.
- Preorder and inorder: `index = {val: i for i, val in enumerate(inorder)}` and `pre = iter(preorder)`. `build(lo, hi)` rebuilds the subtree whose inorder slice is `inorder[lo..hi]`.
- Invariant: each `build()` call consumes exactly the tokens of its own subtree and leaves the rest for its caller.

## Template

```python
class Node:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def decode(data):
    tokens = iter(data.split(","))

    def build():
        token = next(tokens)
        if token == "#":
            return None
        node = Node(int(token))
        node.left = build()
        node.right = build()
        return node

    return build()
```

The matching encoder is the `serialize` method of the worked example.

## What it removes

It removes index bookkeeping and slicing. A shared iterator hands out tokens in pre-order, so no position has to be passed around. The value-to-index map removes the O(n) search for a root in `inorder`, and index ranges remove the O(n) copy of sliced lists.

## Pitfalls

- Leaving out the null markers. Pre-order alone is ambiguous: different shapes give the same value sequence. Writing `#` for every null makes it unique.
- Splitting on a character that can occur in values. Negative numbers contain `-`, so use a comma and parse with `int(token)`.
- Building the right subtree before the left. The shared iterator hands out values in pre-order, so the order of the two `build` calls matters. Swap them and the tree is wrong.
- Preorder and inorder: this needs unique values for the map. With duplicates the index lookup is ambiguous.
- Preorder and inorder: recursing on list slices (`inorder[:mid]`) copies on every call and makes the build O(n^2).
- Fingerprint comparison, if you use it: put a delimiter before every value (`,12`, not `12`), or the string `2` matches inside `12`.
- Deep trees hit Python's recursion limit in `build`; the serialiser here is iterative for that reason.

## Variants

- `serialize-and-deserialize-binary-tree`: pre-order with `#` for nulls and commas between tokens. The `Codec` serialises with a stack and deserialises with a recursive `build()`. Level order also works.
- `construct-binary-tree-from-preorder-and-inorder-traversal`: the next unused preorder value is the root; its position `mid = index[val]` splits the inorder range into left and right. Build left first, then right, over `(lo, mid - 1)` and `(mid + 1, hi)`.
- Subtree comparison by serialisation: `subtree-of-another-tree` is solved in the catalogue by repeated `same-tree` checks, not by serialisation. Serialising both trees with null markers and a leading delimiter, then a substring search, is the faster alternative the solution mentions. See `tree-recursion-return-and-best`.

## Worked example

Problem: `serialize-and-deserialize-binary-tree`

```python
class Codec:
    def serialize(self, root):
        """Encodes a tree to a single string."""
        # Pre-order (node, left, right) with "#" for null. Recording the nulls is what
        # makes the shape unambiguous from one traversal. Iterative to avoid deep
        # recursion; push right first so left is popped (visited) first.
        result = []
        stack = [root]
        while stack:
            node = stack.pop()
            if node is None:
                result.append("#")
            else:
                result.append(str(node.val))
                stack.append(node.right)
                stack.append(node.left)
        # Commas delimit tokens so multi-digit and negative values stay intact.
        return ",".join(result)

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
```

`result` and `stack` in `serialize` are the encoder's setup, and `"#"` is the null marker. In `deserialize`, `tokens` is the shared iterator, and `build()` reads the token, returns `None` for `"#"`, and otherwise builds left then right in the same order the encoder wrote them.
