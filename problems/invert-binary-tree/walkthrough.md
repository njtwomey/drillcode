## The idea

Inverting a tree means mirroring it: at every node the left and right children trade places. A mirror of a tree is the node with its two subtrees swapped, and each of those subtrees is itself mirrored. That is a recursive definition, so write it directly.

## Set-up

There is no extra state. The base case is `root is None`, which returns `None` (nothing to swap). The recursive case:

```python
root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
```

Invariant: `invertTree(x)` returns the root of the mirrored version of `x`, reusing the same nodes.

## Step by step

Start with the tree `4`, children `2` and `7`, and `2` has children `1` and `3`.

```text
before             after
      4                  4
     / \                / \
    2   7              7   2
   / \                    / \
  1   3                  3   1
```

The calls in order (the right side is evaluated first in the code):

```text
invertTree(4)
  invertTree(7)     children None, None -> swap nothing, returns 7
  invertTree(2)
    invertTree(3)   returns 3
    invertTree(1)   returns 1
    2.left, 2.right = 3, 1           returns 2   (2 now has 3 left, 1 right)
  4.left, 4.right = 7, 2             returns 4
```

Each node does the swap after its children are already mirrored, but swapping first would work too.

## Why it works

Assume both subtrees come back correctly mirrored (it holds for `None` and for leaves). Putting the mirrored right subtree on the left and the mirrored left subtree on the right is exactly the mirror of the whole. By induction it holds for the whole tree.

## Where it goes wrong

Splitting the swap into two statements with no temporary. The second line then reads a pointer the first line already overwrote:

```text
root.left = invert(root.right)    left is now overwritten
root.right = invert(root.left)    reads the NEW left: both sides end up equal
```

The tuple assignment avoids this because both right-hand calls run before either attribute is rebound. Also keep the `None` check, or the recursion crashes on leaves.

## Other approaches

An iterative BFS or DFS with a queue or stack does the same swap at each popped node. It avoids deep recursion on a very tall tree.

## Cost

Time O(n): every node is visited and swapped once. Space O(h) for the recursion stack, from log n for a balanced tree to n for a chain.
