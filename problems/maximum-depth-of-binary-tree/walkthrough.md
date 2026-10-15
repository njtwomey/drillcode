## The idea

The depth of a tree is the number of nodes on the longest path from the root down. The root adds one level, and below it sits the deeper of its two subtrees. So `depth(tree) = 1 + max(depth(left), depth(right))`, and an empty tree has depth 0. The recursion follows that definition directly.

## Set-up

No variables besides the recursion itself. Base case: `root is None` returns 0.

Invariant: `maxDepth(x)` returns the number of levels in the subtree rooted at `x`.

## Step by step

```text
      3
     / \
    9   20
       /  \
      15   7
```

```text
maxDepth(3)
  maxDepth(9)
    maxDepth(None) -> 0
    maxDepth(None) -> 0
    1 + max(0, 0) = 1
  maxDepth(20)
    maxDepth(15)  -> 1     (two None children)
    maxDepth(7)   -> 1
    1 + max(1, 1) = 2
  1 + max(1, 2) = 3
```

The answer is 3: the paths 3-20-15 and 3-20-7 have three nodes.

## Why it works

Every path from the root goes through the left or the right child, so the longest path is the longer of the two subtree paths, plus the root. Subtrees are strictly smaller, so the recursion reaches the `None` base case.

## Where it goes wrong

Returning 1 for a `None` node instead of 0 makes every depth too large by one. A leaf should be `1 + max(0, 0) = 1`:

```text
wrong base case (None -> 1):  leaf = 1 + max(1, 1) = 2   one level too many
```

Another slip is using `max` on the counts of nodes rather than depth: adding the sizes of both sides counts the whole tree.

## Other approaches

Level-order BFS counts how many levels it takes to empty the queue, with the same O(n) time. It avoids deep recursion on a very tall tree.

## Cost

Time O(n): each node is visited once. Space O(h) for the call stack: about log n for a balanced tree, n for a chain.
