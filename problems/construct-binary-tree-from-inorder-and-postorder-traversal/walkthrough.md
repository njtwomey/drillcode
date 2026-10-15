## The idea

Postorder visits left, right, then root. So the last value in postorder is the root of the whole tree. Inorder visits left, root, right, so once you know the root's value, everything to its left in inorder is the left subtree and everything to its right is the right subtree. Two lists, each telling you what the other does not.

That gives a recursion: find the root, split inorder around it, build both sides. The only subtlety is how to peel off roots for the sub-trees.

## Set-up

- `index` maps each value to its position in `inorder`. Values are unique, so finding the split is O(1) instead of a scan.
- `post = iter(reversed(postorder))` hands out roots one at a time. Read backwards, postorder is root, right subtree, left subtree.
- `build(lo, hi)` rebuilds the subtree whose values are `inorder[lo..hi]`. If `lo > hi` the slice is empty and there is no node.

Because one shared iterator is consumed, the order of calls matters: right first, then left.

## Step by step

`inorder = [9,3,15,20,7]`, `postorder = [9,15,7,20,3]`. The iterator yields 3, 20, 7, 15, 9.

```text
build(0,4)  next = 3, mid = 1
├─ right: build(2,4)  next = 20, mid = 3
│   ├─ right: build(4,4)  next = 7, mid = 4
│   │   ├─ right: build(5,4)  empty ─▶ None
│   │   └─ left:  build(4,3)  empty ─▶ None
│   └─ left:  build(2,2)  next = 15, mid = 2
│       └─ both sides empty
└─ left:  build(0,0)  next = 9, mid = 0
    └─ both sides empty

result:        3
              / \
             9   20
                /  \
               15   7
```

The inorder slice shrinks around each root:

```text
inorder:  [ 9 | 3 | 15  20  7 ]        root 3 at index 1
                    [15 | 20 | 7]      root 20 at index 3
```

## Why it works

In reversed postorder, a root comes before every node in its subtrees, and the whole right subtree comes before the whole left subtree. So when `build` is called for a slice, the next unused value is exactly that slice's root. After the right call returns, the iterator has consumed exactly the right subtree's values, so the next value is the left subtree's root.

## Where it goes wrong

Building left before right. The iterator then gives the right subtree's root to the left subtree:

```text
wrong:  build(0,4) takes 3, then left build(0,0) takes 20 (should be 9)
```

The other trap is the base case: an empty slice (`lo > hi`) must return `None` without consuming from the iterator.

## Cost

Time O(n): every node is created once and the map makes each split O(1). Space O(n) for the map, plus recursion depth up to n for a skewed tree.
