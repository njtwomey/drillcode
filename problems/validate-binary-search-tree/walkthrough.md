## The idea

A binary search tree is not just "left child is smaller than its parent and right child is larger". Every node in the left subtree must be smaller than the root, and every node in the right subtree must be larger, all the way down. Checking only parent against child misses cases where a deep node breaks a rule set by a distant ancestor.

So each node gets a window of allowed values, and the window is built from all its ancestors. The root may be anything. Going left, the node's value becomes the new upper limit. Going right, it becomes the new lower limit. A node is valid if its value sits strictly inside the window.

## Set-up

- `stack` holds work items `(node, low, high)`. Each says "this node must satisfy `low < node.val < high`".
- It starts as `[(root, None, None)]`. `None` means unbounded on that side. This avoids picking a sentinel like infinity that a node value could equal.
- The loop is iterative, so a tall skewed tree cannot hit the recursion limit.

```text
tree:        5
           /   \
          4     6
               / \
              3   7

stack = [ (5, None, None) ]
```

## Step by step

Children are pushed left first, then right, so the right one is popped first.

```text
pop (5, None, None)   no bounds, ok
    push (4, None, 5)    left: must be < 5
    push (6, 5, None)    right: must be > 5

pop (6, 5, None)      5 < 6, ok
    push (3, 5, 6)       left of 6: between 5 and 6
    push (7, 6, None)    right of 6: > 6

pop (7, 6, None)      6 < 7, ok
    push two None children, which are skipped when popped

pop (3, 5, 6)         3 <= low (5)  ->  return False
```

Node 3 is a perfectly good left child of 6. The parent check alone would pass. But it lives in the right subtree of 5, so it must exceed 5, and the inherited `low = 5` catches it.

## Why it works

Each node's window is the intersection of every ancestor's constraint: the tightest lower bound among ancestors it is to the right of, and the tightest upper bound among those it is to the left of. Passing `(low, node.val)` to the left child and `(node.val, high)` to the right child keeps that window exact, since the other bound is just inherited. If every node is strictly inside its window, the BST property holds everywhere.

## Where it goes wrong

- Comparing only with the immediate parent, as in the example above.
- Using `<` and `>` in the rejection test. The code uses `<=` and `>=` so that duplicates are rejected. `[2, 2, 3]` and `[2, 1, 2]` are both invalid.
- Using `float("-inf")` or `-2**31` as the sentinel. A node holding `-2147483648` would then fail its own bound. `None` avoids that.

## Other approaches

An in-order traversal of a BST visits values in strictly increasing order. Walk the tree in order, remember the previous value, and fail if any value is not greater than it. It uses the same O(h) space and is just as short.

## Cost

Time O(n): each node is visited once. Space O(h) for the stack, where h is the tree height. That is about log n for a balanced tree and n for a skewed one.
