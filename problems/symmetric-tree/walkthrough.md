## The idea

A tree is symmetric when its left half is a mirror image of its right half. "Mirror image" is a relation between two trees, so the problem is really about comparing two subtrees, `a` and `b`, not about one tree.

Two trees mirror each other when their roots have equal values, and the left child of one mirrors the right child of the other, and vice versa. That sentence is the whole solution. A tempting shortcut, checking that each level reads as a palindrome, fails because it ignores where the gaps are.

## Set-up

There are no running variables. The helper `mirror(a, b)` answers "is `a` the reflection of `b`?" and has three outcomes:

- both `None`: yes, two empty trees mirror each other.
- exactly one `None`, or the values differ: no.
- otherwise recurse, pairing outer with outer and inner with inner.

The top-level call is `mirror(root.left, root.right)`, and an empty tree is symmetric.

## Step by step

```text
        1
       / \
      2   2
     / \ / \
    3  4 4  3
```

```text
mirror(2L, 2R)            values 2 == 2
  mirror(3, 3)            outer pair: 2L.left with 2R.right. 3 == 3
    mirror(None, None)    True
    mirror(None, None)    True
  mirror(4, 4)            inner pair: 2L.right with 2R.left. 4 == 4
    mirror(None, None)    True
    mirror(None, None)    True
result: True
```

Now a tree that has the same values on each level but the wrong shape:

```text
        1
       / \
      2   2
       \   \
        3   3
```

```text
mirror(2L, 2R)            2 == 2
  mirror(None, 3)         outer pair: 2L.left is None, 2R.right is 3
                          exactly one side missing -> False
result: False
```

The first call fails before the inner pair is even looked at, because `and` short-circuits.

## Why it works

The recursion encodes the definition. Reflecting a tree swaps left and right at every level, so the outer child of one side lands opposite the outer child of the other. Each call checks one pair of positions, and a pair that disagrees on presence or value ends the search.

## Where it goes wrong

Pairing `a.left` with `b.left` is the common mistake. That is a plain equality check (Same Tree), not a mirror check, and it would call the first tree above asymmetric.

In the second tree, the level lists are `[2, 2]` then `[3, 3]`, both palindromes, yet the tree is not symmetric. Only a check that sees the `None` placeholders catches it.

## Cost

Time O(n): each node is visited at most once, as part of one pair. Space O(h) for the recursion, where `h` is the tree height (up to `n` for a chain, though a symmetric chain cannot exist beyond the root).
