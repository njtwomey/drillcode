## The idea

We want every root-to-leaf path whose values add up to `targetSum`. A depth-first walk visits every path naturally. The two things to get right are bookkeeping (what is the current path, and how much of the target is left) and the stopping rule (only a leaf can finish a path).

Instead of building a new list for each path, keep one shared list that grows when we go down and shrinks when we come back up. That is backtracking.

## Set-up

- `path`: the values from the root to the node being visited. Invariant: when `dfs(node, ...)` starts, `path` holds the ancestors of `node`; when it returns, `path` is back to exactly that.
- `remaining`: the target minus the values already on the path. It is passed down as an argument, so each call has its own copy and nothing needs undoing.
- `result`: the finished paths.
- A match needs `node.left is None and node.right is None and remaining == 0`. Matching at a non-leaf does not count.

```text
tree:            5          targetSum = 12
               /   \
              4     7
            /   \
           3     1

path = []      result = []
```

## Step by step

Each call appends its value, subtracts it from `remaining`, then either records a leaf match or recurses into both children, and finally pops.

```text
dfs(5, 12)   path=[5]        remaining=7   not a leaf
  dfs(4, 7)  path=[5,4]      remaining=3   not a leaf
    dfs(3, 3) path=[5,4,3]   remaining=0   leaf, match -> record [5,4,3]
              pop            path=[5,4]
    dfs(1, 3) path=[5,4,1]   remaining=2   leaf, no match
              pop            path=[5,4]
    pop 4                    path=[5]
  dfs(7, 7)  path=[5,7]      remaining=0   leaf, match -> record [5,7]
              pop            path=[5]
  pop 5                      path=[]
```

The result is `[[5,4,3], [5,7]]`.

## Why it works

Every root-to-leaf path is a unique sequence of left or right choices, and the recursion takes every one. The shared `path` is correct at each call because every push is paired with a pop on every exit route. `remaining` tells us the sum so far without re-adding the path. The copy `path[:]` freezes the matching path before later calls change the list.

## Where it goes wrong

- Appending `path` itself. It is the same list object that is emptied later, so the result would end up as lists of nothing.
- Forgetting to pop, or popping only on one branch. The next sibling would start with a stale prefix.
- Recording a match at a non-leaf. With a tree `[1, 2]` and target `1`, the path `[1]` sums to 1 but node 1 has a child, so it is not a root-to-leaf path.

```text
tree 1 ── 2      targetSum = 1
  at node 1: remaining = 0, but left child exists -> not recorded
  at node 2: remaining = -2                       -> not recorded
  result = []
```

## Cost

Time O(n^2) in the worst case: n nodes visited, and each matching path costs up to O(n) to copy. A balanced tree is closer to O(n log n). Space O(h) for the recursion and `path`, where `h` is the tree height, not counting the output.
