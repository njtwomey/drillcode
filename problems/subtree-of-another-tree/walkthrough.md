## The idea

To ask "does `subRoot` appear somewhere inside `root`?", you need two small questions. The first: are these two trees identical? That is the Same Tree check, here called `_same`. The second: where in the big tree should we try that check? The answer is "everywhere". Every node of `root` is a candidate match point, so we try the check at one node, and if it fails we move on to its children.

The match must be exact. A subtree includes all the descendants below its top node, so a node with the right value but extra children underneath does not count.

The brute force is already the answer here: try every node, compare cheaply, and stop early on the first mismatch. The faster alternative (serialise both trees and do a substring search) is mentioned at the end.

## Set-up

There are no variables, only two recursive functions:

- `isSubtree(root, subRoot)` walks the main tree. It returns `True` as soon as one node matches.
- `_same(a, b)` compares two trees node for node, shape and values.

Two base cases in `isSubtree` matter. An empty `subRoot` is a subtree of anything. An empty `root` (with a non-empty `subRoot`) means we ran out of tree without a match.

## Step by step

Main tree `3 / (4 / (1, 2)) / 5`, looking for `4 / (1, 2)`:

```text
        3              sub:    4
       / \                    / \
      4   5                  1   2
     / \
    1   2
```

```text
isSubtree(3)   _same(3, 4)   3 != 4          False
  isSubtree(4) _same(4, 4)   equal
                 _same(1, 1)  equal, both children None   True
                 _same(2, 2)  equal, both children None   True
               returns True
  or short-circuits: right side (5) is never visited
```

Now a main tree where node 2 has an extra child `0`:

```text
        3              _same(4, 4)   equal
       / \               _same(1, 1)   True
      4   5              _same(2, 2)   equal values, then
     / \                   _same(None, 0)   one side missing -> False
    1   2                returns False
       /
      0                  so isSubtree moves on to 1, 2, 0, 5: nothing matches
                         result: False
```

## Why it works

If `subRoot` occurs in `root`, then there is a node in `root` whose entire subtree is identical to it. The walk reaches every node, and `_same` is true exactly for that node. If there is no such node, no `_same` call can succeed.

## Where it goes wrong

Comparing only values down to the end of `subRoot` is the classic bug: it would accept the second example above. `_same` must also reject when one side still has a child and the other does not, which the `a is None or b is None` line does.

Forgetting that the root of the whole tree may itself be the match is the other slip. That is why `_same(root, subRoot)` is tried before recursing.

## Other approaches

Serialise each tree with a marker for missing children (with a separator before each value so `1` and `11` stay distinct), then check whether one string is a substring of the other. That can be linear with a good substring search.

## Cost

Time O(m * n) for `m` main nodes and `n` subtree nodes: each main node starts at most one `_same` of cost up to `n`, though most fail on the first comparison. Space O(h) for the recursion stack, where `h` is the height of the main tree.
