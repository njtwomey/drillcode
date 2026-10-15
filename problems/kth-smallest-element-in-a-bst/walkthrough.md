## The idea

In a binary search tree, everything in a node's left subtree is smaller than the node and everything in the right subtree is larger. Visiting left, then node, then right (in-order) therefore produces the values in ascending order. The kth smallest value is just the kth node visited, so we walk in order and stop at the kth.

Collecting all values and sorting is wasteful. Walking in order gives sorted output for free, and stopping early means we only touch what we need.

## Set-up

- `stack` holds the ancestors whose left subtree we are currently inside. Their turn comes after the left subtree is done. Its size never exceeds the tree height.
- `node` is the cursor: either the next node to dive from, or `None` when we have just run off a leaf.
- `k` is counted down; reaching 0 means we have visited `k` nodes.

```text
tree:         5
            /   \
           3     6
          / \
         2   4
        /
       1                k = 3

in-order is 1, 2, 3, 4, 5, 6
```

## Step by step

Each outer round does two things: dive left pushing every node, then pop one node (visit it), decrement `k`, and move to its right child.

```text
start        node=5, stack=[]
dive left    push 5, 3, 2, 1          stack=[5,3,2,1]  node=None
pop 1        k: 3 -> 2                visit #1 = 1
             node = 1.right = None    stack=[5,3,2]
(no dive)    node is None, so skip to pop
pop 2        k: 2 -> 1                visit #2 = 2
             node = 2.right = None    stack=[5,3]
pop 3        k: 1 -> 0                visit #3 = 3  -> return 3
```

If we needed more, the walk would continue: after popping 3 it would move to `3.right`, dive from node 4, and so on.

```text
stack over time (top on the right):
 [5 3 2 1] -> [5 3 2] -> [5 3] -> done at 3
```

## Why it works

The stack always holds exactly the nodes that were passed on the way down and have not been visited yet. Popping gives the leftmost unvisited node, which is the smallest remaining value, because everything smaller lives in subtrees already finished. After visiting it, the next larger values are in its right subtree, so we go there.

## Where it goes wrong

- Moving to `node.right` before decrementing `k`, or forgetting to reset `node` after a pop. The right move must come last, and it is also what makes the next round dive correctly.
- Checking `k == 0` before the pop would return the wrong node.
- The loop condition needs both `node` and `stack`. When the cursor is `None` but ancestors remain, we still have to pop.
- The final `return -1` is unreachable for valid `k`; it only keeps the function total.

## Cost

Time O(h + k): the first dive costs up to the height `h`, then each of the `k` visits adds amortised constant work. Space O(h) for the stack. A recursive version uses the same space as call-stack frames.
