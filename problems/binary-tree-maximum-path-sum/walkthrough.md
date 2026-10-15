## The idea

A path in a tree can go up from one node, bend at a single highest node, and come down the other side. Every path has exactly one top node. So if you can answer, for each node, "what is the best path that bends here", the largest of those is the overall answer.

For that you need, from each child, the best path that goes only straight down from it. A path that continues upward to a parent can only pick one branch, so a node reports a single downward arm to its parent. But it uses both arms when it is the bend itself.

## Set-up

Two separate quantities are in play:

- `best` is the answer so far: the best path seen that bends at some node. It starts at negative infinity (not 0) so a tree of all negative numbers still returns its largest single value.
- `gain(node)` returns the best path that starts at `node` and goes only down. It is what a parent may add to its own path.

Inside `gain`, `left` and `right` are the children's gains clamped at 0: a negative branch only hurts, so treat it as "do not take it". A missing node contributes 0.

```text
         -10
        /   \
       9     20
            /  \
           15   7
```

## Step by step

This is a post-order walk, so children finish before parents.

```text
gain(9):   left=0, right=0.   best = max(-inf, 9)       = 9
           returns 9

gain(15):  left=0, right=0.   best = max(9, 15)         = 15
           returns 15

gain(7):   left=0, right=0.   best = max(15, 7)         = 15
           returns 7

gain(20):  left=15, right=7.  bend: 20 + 15 + 7         = 42
           best = 42
           returns 20 + max(15, 7) = 35

gain(-10): left=9, right=35.  bend: -10 + 9 + 35        = 34
           best stays 42
           returns -10 + 35 = 25
```

The answer is 42, the path 15, 20, 7. The root was not on it. The root's best bend was 34, lower than the path that avoids it.

## Why it works

Every path has a unique top node. At that node the best path is the node's value plus the best downward arm on each side, which is exactly `node.val + left + right`. Computing it at every node covers every possible top. The return value gives parents only a single arm, since a path that keeps going up cannot fork.

## Where it goes wrong

- Returning `node.val + left + right` upward. That would let the path fork at the child and again at the parent, which is not a path.
- Not clamping at 0. A branch with a negative sum would be forced into the total.
- Initialising `best` to 0. With `[-3]` the answer must be -3, and with `[-3, -2, -1]` it must be -1. Zero would make the code answer 0, a path that does not exist.

```text
[-3, -2, -1]   root -3, left -2, right -1
gain(-2): best = -2     gain(-1): best = -1
root: left = max(0, -2) = 0, right = 0, bend = -3.  best stays -1.
```

## Cost

Time O(n): each node visited once. Space O(h) for the recursion, with h the tree height.
