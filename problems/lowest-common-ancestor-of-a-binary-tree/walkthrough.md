## The idea

Without ordering we cannot choose a side, so we look at both. Each recursive call answers one question about its subtree: "which of `p` and `q`, if any, did you find?" A node that hears a hit from its left and a hit from its right is where the two paths meet, so it is the answer.

## Set-up

There are no variables to initialise, only the recursion:

- Base case: if `root` is `None`, or is `p` or `q`, return `root` immediately.
- `left` and `right` hold what each child subtree reported.
- Return value: `None` (neither found), a target node (one found), or the LCA (both found below).

Why stop early at `p` or `q`? If the other target is below it, this node is the LCA anyway (a node is its own ancestor). If not, there is nothing more to learn.

## Step by step

```text
        3
      /   \
     5     1
    / \   / \
   6   2 0   8
      / \
     7   4
```

Take `p = 7`, `q = 4`. Calls run left subtree first.

```text
lca(3)
  lca(5)
    lca(6)
      lca(None) -> None
      lca(None) -> None
    6: left None, right None       returns None
    lca(2)
      lca(7)                       7 is p        returns 7
      lca(4)                       4 is q        returns 4
    2: left 7 and right 4          both set      returns 2
  5: left None, right 2            returns left or right = 2
  lca(1)
    ... (0 and 8 found nothing)    returns None
  3: left 2, right None            returns 2
```

The answer is node 2. Note how the value `2` travels up unchanged through `5` and `3`, because only one side had anything to report.

If instead `p = 5`, `q = 4`: `lca(5)` returns `5` at once without visiting node 2 or its children. At the root, `left = 5` and `right = None`, so `5` is returned, which is right because 4 sits below 5.

## Why it works

For any node, the number of targets in its subtree is the sum of the numbers in its two child subtrees (plus itself). The first node, going bottom-up, that holds both targets is the lowest common ancestor. Seeing both targets reported from different children detects exactly that node. When the early return fires, the target's own subtree is treated as a single hit, which is enough because the other target either is below it or is found elsewhere.

## Where it goes wrong

Returning `root` when only one side is non-null would be a mistake; you must pass the child's result up. Also, comparing with `is` (node identity), as the code does, avoids confusing two nodes that share a value.

## Cost

Time O(n): every node may be visited once. Space O(h) for the recursion stack, up to O(n) on a chain-shaped tree.
