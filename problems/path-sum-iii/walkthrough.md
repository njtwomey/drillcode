## The idea

A downward path can start at any node, so the obvious plan is to start a fresh search from every node and count the paths that hit the target. That works, but a tall skinny tree makes it O(n²).

The better view is to treat each root-to-node route like an array and use prefix sums. Let `prefix` be the sum of all values from the root down to the current node. A downward path that ends here and sums to `targetSum` starts just below some ancestor whose own prefix was `prefix - targetSum`. So instead of searching, we look that number up in a hash map.

## Set-up

- `seen` maps a prefix sum to how many nodes on the current root-to-node route have that prefix. It starts as `{0: 1}`: the empty prefix before the root, which lets a path begin at the root itself.
- `prefix` is passed down the recursion, so each call knows the sum from the root to its parent.
- `count` collects the matches found at this node plus everything below it.

The invariant: while visiting a node, `seen` describes exactly its ancestors, nothing else.

```text
tree:        10
            /  \
           5    -3        targetSum = 8
          /       \
         3         11

seen = {0: 1}        prefix = 0 (before the root)
```

## Step by step

Order of visits: 10, 5, 3, then back up, then -3, 11. At each node we first look up `prefix - targetSum`, then add `prefix` to `seen`.

```text
node  prefix  look up (prefix-8)  hits   seen afterwards
10      10          2               0     {0:1, 10:1}
 5      15          7               0     {0:1, 10:1, 15:1}
 3      18         10               1     {0:1, 10:1, 15:1, 18:1}
                                          path 5 -> 3 sums to 8
leave 3, leave 5 (decrement 18, 15)       {0:1, 10:1}
-3       7         -1               0     {0:1, 10:1, 7:1}
11      18         10               1     {0:1, 10:1, 7:1, 18:1}
                                          path -3 -> 11 sums to 8
```

Total: 2 paths.

## Why it works

If the prefix at an ancestor is `a` and the prefix here is `p`, the nodes strictly below that ancestor down to here sum to `p - a`. We want that to equal `targetSum`, so `a = p - targetSum`. `seen` counts how many ancestors have that prefix, and each one is a different starting point, so the count is the number of matching paths ending here. Negative values and zeros are fine because we count with a dictionary, not a sliding window.

## Where it goes wrong

Forgetting `seen[prefix] -= 1` on the way out leaves the left subtree's prefixes in the map while the right subtree runs. Those nodes are not ancestors, so the right side would count paths that jump sideways.

```text
No decrement, targetSum = 3, at node 11 (prefix 18):
  look up 15  -> finds node 5's prefix, left over from the other branch
  but 5 is not an ancestor of 11, so this "path" does not exist.
```

Seeding `seen` without `{0: 1}` misses every path that begins at the root.

## Cost

Time O(n): each node does one lookup and two updates. Space O(h) for the recursion and the map, since the map only ever holds the current route.
