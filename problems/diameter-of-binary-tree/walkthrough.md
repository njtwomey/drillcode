## The idea

The diameter is the number of edges on the longest path between any two nodes. Any such path has a highest node, the one where it turns around. At that node the path goes down the left side as far as it can and down the right side as far as it can, so its length is `left height + right height`.

That suggests the plan: compute subtree heights bottom-up, and at every node also ask what the longest path bending there would be. The answer is the largest of those.

The path does not have to pass through the root, which is why we check every node, not just the top one.

## Set-up

- `best` is the longest path found so far, counted in edges. It starts at 0 (a single node has diameter 0).
- `height(node)` returns the height of the subtree in nodes (an empty tree is 0) and updates `best` as a side effect. `nonlocal best` lets the inner function change the outer variable.

Invariant: when `height(node)` returns, `best` is at least the longest path that lies entirely inside that subtree.

## Step by step

Tree `1` with children `2` and `3`, and `2` has children `4` and `5`:

```text
        1
       / \
      2   3
     / \
    4   5

height(1)
  height(2)
    height(4): left=0 right=0  best=max(0,0)=0   returns 1
    height(5): left=0 right=0  best=0            returns 1
    at 2: left=1 right=1  best=max(0,2)=2        returns 2
  height(3): left=0 right=0  best=2              returns 1
  at 1: left=2 right=1  best=max(2,3)=3          returns 3
```

`best = 3`, the path 4 - 2 - 1 - 3.

Note what each node reports upward: only `1 + max(left, right)`, the taller single branch. A parent can extend one branch downward, not both, so reporting the sum would be wrong.

## Why it works

Every path has a unique top node, and at that node its length is at most `left + right` (heights are the longest downward runs). The code evaluates that quantity at every node, so the true longest path is among the candidates, and no candidate exceeds it since each one is a real path.

## Where it goes wrong

Only looking at the root. Here the longest path lies wholly inside the left subtree, and the path through the root is shorter:

```text
            1
           /
          2              root: left = 3, right = 0 -> 3 edges
         / \
        3   4            node 2: left = 2, right = 2 -> 4 edges (best)
       /     \
      5       6          path: 5 - 3 - 2 - 4 - 6
```

Also be careful about units. Heights here are counted in nodes (empty is 0), so `left + right` is already the edge count of the path through the node. Do not add 1 or 2.

## Cost

Time O(n): each node is visited once. Space O(h) for the recursion stack, up to O(n) on a chain.
