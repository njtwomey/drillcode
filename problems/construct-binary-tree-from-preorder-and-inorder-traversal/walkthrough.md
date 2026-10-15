## The idea

Preorder visits root, left subtree, right subtree. So the first value in preorder is the root of the whole tree. Inorder visits left, root, right, so once you find the root's value in inorder, everything to its left is the left subtree and everything to its right is the right subtree.

Each list alone is ambiguous; together they pin the tree down. The recursion writes itself: take the next root from preorder, split inorder around it, build the left side, then the right side.

## Set-up

- `index` maps value to its position in `inorder`. Values are unique, so finding the split point is O(1) instead of a scan.
- `pre = iter(preorder)` hands out roots left to right. Preorder is consumed strictly in order: a root, then its entire left subtree, then its entire right subtree.
- `build(lo, hi)` builds the subtree whose values are `inorder[lo..hi]`. When `lo > hi`, the slice is empty: no node, return `None`.

## Step by step

`preorder = [3,9,20,15,7]`, `inorder = [9,3,15,20,7]`:

```text
build(0,4)   next from pre = 3,  mid = 1
│            inorder:  [ 9 | 3 | 15 20 7 ]
├─ left:  build(0,0)   next = 9,  mid = 0
│          both sides empty, a leaf
└─ right: build(2,4)   next = 20, mid = 3
           inorder slice: [ 15 | 20 | 7 ]
           ├─ left:  build(2,2)  next = 15  leaf
           └─ right: build(4,4)  next = 7   leaf
```

The iterator hands out 3, 9, 20, 15, 7 in that order, which is the preorder list. The result:

```text
        3
       / \
      9   20
         /  \
        15   7
```

## Why it works

For any slice, the next unused preorder value is its root: preorder lists a root before anything in its subtrees. The inorder position splits the slice into left and right parts. Building the left part consumes exactly as many preorder values as the left part has nodes, so when the right part starts, the iterator sits at the right subtree's root.

## Where it goes wrong

Building right before left. The iterator is shared, and preorder lists the left subtree first:

```text
wrong:  build(0,4) takes 3, then right build(2,4) takes 9   (9 is not in that slice)
right:  left first, so 9 goes to the left slice
```

The other classic slip is searching `inorder` for the root with `list.index` each time. It works but turns the algorithm into O(n^2) on a skewed tree; the map avoids that. A left-skewed tree like `preorder = [1,2,3]`, `inorder = [3,2,1]` recurses to depth n.

## Cost

Time O(n): each node is built once and the lookup is O(1). Space O(n) for the map, plus recursion depth up to n.
