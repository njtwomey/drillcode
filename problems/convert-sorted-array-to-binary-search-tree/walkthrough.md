## The idea

A binary search tree (BST) keeps smaller values on the left of each node and larger on the right. A sorted array is already the in-order reading of such a tree, so we only have to pick which element is the root. To keep the tree height balanced, choose the middle element: about half the values go left and half go right, and the same rule applies recursively inside each half.

## Set-up

- `build(lo, hi)` makes a tree from `nums[lo..hi]` (inclusive) and returns its root, or `None` when `lo > hi`.
- Passing indices instead of slicing means no list copies.

Invariant: each call receives a contiguous sorted range and returns a valid BST of exactly those values whose two subtree sizes differ by at most one.

```text
nums:  -10  -3   0   5   9
idx:     0   1   2   3   4
         ^               ^
         lo              hi        build(0, 4)
```

## Step by step

```text
build(0, 4)  mid = 2  -> node 0
  build(0, 1)  mid = 0  -> node -10
    build(0, -1) -> None            (left of -10)
    build(1, 1)  mid = 1  -> node -3
      build(1, 0) -> None           (left of -3)
      build(2, 1) -> None           (right of -3)
  build(3, 4)  mid = 3  -> node 5
    build(3, 2) -> None             (left of 5)
    build(4, 4)  mid = 4  -> node 9
      build(4, 3) -> None
      build(5, 4) -> None
```

The result:

```text
          0
         / \
      -10   5
         \   \
         -3   9
```

For an even-length range, `(lo + hi) // 2` takes the lower middle, which is why `-10` (not `-3`) is chosen for `[-10, -3]`. Either middle gives a valid answer.

## Why it works

Everything in `lo..mid-1` is smaller than `nums[mid]` and everything in `mid+1..hi` is larger, because the input is sorted. So the BST property holds at every node. The two halves have sizes that differ by at most one, so heights differ by at most one at every level, which is height balanced.

## Where it goes wrong

Using `mid` in a child range puts the root in its own subtree and recurses forever. The children must be `build(lo, mid - 1)` and `build(mid + 1, hi)`:

```text
wrong: build(lo, mid)   range [0,0] -> mid = 0 -> build(0, 0) again ...
```

Slicing (`nums[:mid]`) also works but copies lists and makes the cost O(n log n).

## Cost

Time O(n): one node created per element. Space O(log n) for the recursion, since the depth is about log2(n) (the output tree itself is not counted).
