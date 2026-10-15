## The idea

A tree is balanced when, at every node, the two subtrees differ in height by at most one. The obvious plan is to write a `height` function and call it at every node to compare the two sides. That works, but it re-measures the same subtrees again and again: on a long chain it costs O(n^2).

The fix is to notice that computing a height already visits every node below. So let the height function do the balance check on the way back up. Each call returns the height, or `-1` as a flag meaning "something below me is already unbalanced". One pass, and each node is looked at once.

## Set-up

There is only the inner function `height(node)` and its return contract:

- It returns the height of the subtree (an empty subtree is 0).
- It returns `-1` if any node in that subtree broke the rule.
- `-1` is safe as a flag because real heights are never negative.

There is no loop state. The recursion bottoms out at `None`, which returns 0.

## Step by step

Take a left-leaning chain `1 ← 2 ← 3` (1 is the root, 2 its left child, 3 the left child of 2). The calls go down first, and the answers come back up:

```text
        1
       /
      2
     /
    3

height(1)
  height(2)
    height(3)
      height(None) -> 0      (left of 3)
      height(None) -> 0      (right of 3)
      |0 - 0| = 0 ok         returns 1
    left = 1
    height(None) -> 0        (right of 2)
    |1 - 0| = 1 ok           returns 2
  left = 2
  height(None) -> 0          (right of 1)
  |2 - 0| = 2 > 1            returns -1
```

The root gets `-1`, so `isBalanced` returns `False`. Now a healthy tree, `3` with children `9` and `20`:

```text
height(3)
  height(9)  -> 1
  height(20) -> 1
  |1 - 1| = 0 ok   returns 2        -> 2 != -1, so True
```

If the left side had already returned `-1`, the code returns `-1` at once and never explores the right side.

## Why it works

For any node, "balanced" means its left subtree is balanced, its right subtree is balanced, and their heights are within one. `height` checks exactly those three things in that order. Once a `-1` appears it is passed straight up, so the root sees it. A tree with no violations never produces `-1`, because each returned value is then a real height.

## Where it goes wrong

Forgetting to propagate the flag is the classic bug. If a child returned `-1` and you computed `abs(left - right)` anyway, the `-1` would behave like a height and could even look balanced:

```text
left = -1 (unbalanced below), right = 0
abs(-1 - 0) = 1   -> looks fine, returns 1 + max(-1, 0) = 1   WRONG
```

That is why the code checks `left == -1` and `right == -1` before trusting the numbers. Checking only differences at the current node, without looking at the subtrees, is the other common mistake: a tree can be balanced at the root and broken deeper down.

## Cost

Time O(n): each node is visited once. Space O(h) for the recursion stack, where h is the tree height (up to n for a chain).
