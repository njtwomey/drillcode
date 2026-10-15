## The idea

Two trees are the same when they have the same shape and the same value at every position. That description is already recursive: two trees are equal if their roots match, their left subtrees are equal, and their right subtrees are equal. So walk both trees in lockstep and stop at the first disagreement.

## Set-up

There is no stored state; each call looks at one pair `(p, q)`: the nodes at the same position in each tree. Three outcomes are possible for a pair:

- Both are `None`: the trees ran out together, so this position agrees.
- Exactly one is `None`, or the values differ: they disagree, return `False`.
- Both exist with equal values: the answer depends on the children.

The `None` checks come before any `.val` access, otherwise we would read an attribute from `None`.

## Step by step

Compare `p = [1, 2, 3]` with `q = [1, 2, 4]`:

```text
    p:  1          q:  1
       / \            / \
      2   3          2   4
```

```text
isSameTree(1, 1)           values equal, check children
  isSameTree(2, 2)         values equal, check children
    isSameTree(None, None)   ──▶ True
    isSameTree(None, None)   ──▶ True
  2 returns True
  isSameTree(3, 4)         3 != 4                   ──▶ False
1: left was True, right was False   ──▶ False
```

The `and` between the two recursive calls means that the right side is only checked when the left is fine, and that a single `False` anywhere makes the whole result `False`.

A shape difference is caught the same way. For `[1, 2]` against `[1, null, 2]`:

```text
isSameTree(1, 1)           equal
  isSameTree(2, None)      one side missing   ──▶ False
```

## Why it works

If the trees are identical, every pair reached is either both `None` or two equal nodes, so every call returns `True` and the result is `True`. If they differ at any position, the recursion reaches that position, because every position above it matched, and that call returns `False`, which `and` carries all the way up.

## Where it goes wrong

Order of the checks. Testing `p.val != q.val` before the `None` checks crashes when a node has no counterpart.

```text
isSameTree(2, None):
   p.val != q.val   ──▶ AttributeError on None
```

Another subtle mistake is only testing `p is None or q is None` and returning `True`, which would treat "one is missing" as a match. The two cases (both `None` versus exactly one) must be separated, and that is what the first two `if` statements do. Two empty trees correctly return `True`.

## Cost

Time O(n) for n nodes in the smaller tree (it stops at the first mismatch). Space O(h) for the recursion stack, where h is the tree height.
