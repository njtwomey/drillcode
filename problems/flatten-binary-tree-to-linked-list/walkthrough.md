## The idea

Flattening means rewriting the tree in place so that every node's `left` is empty and `right` points to the next node in preorder (node, then left subtree, then right subtree).

The recursive idea is "flatten the left, flatten the right, stitch". There is a way to do it with no recursion and no stack. For a node with a left child, in preorder the whole left subtree comes before the right subtree. So the right subtree should hang off the very last node of the left subtree. Do that splice, slide the left subtree into the `right` slot, and move on. Each node ends up needing only the same operation.

## Set-up

- `curr` is the node being processed. It starts at `root`.
- `tail` is a temporary pointer to the rightmost node of `curr.left`, the node that will be last in preorder before the old right subtree.

Invariant: everything before `curr` in preorder is already a chain of right pointers with no left children.

```text
        1
       / \
      2   5
     / \   \
    3   4   6

curr = 1
```

## Step by step

```text
curr = 1   has a left child (2).
           tail: start at 2, go right -> 4.
           tail.right = curr.right  ->  4.right = 5
           curr.right = curr.left   ->  1.right = 2
           curr.left  = None

        1
         \
          2
         / \
        3   4
             \
              5
               \
                6
           curr = curr.right = 2

curr = 2   has a left child (3).
           tail: start at 3, no right child, so tail = 3.
           3.right = 2.right = 4
           2.right = 3,  2.left = None

        1 ──▶ 2 ──▶ 3 ──▶ 4 ──▶ 5 ──▶ 6
           curr = 3
```

For `curr = 3, 4, 5, 6` there is no left child, so nothing changes; `curr` just walks right. When it reaches `None` the loop ends. The chain is `1, 2, 3, 4, 5, 6`, which is the preorder.

## Why it works

Every splice puts the old right subtree after the last node of the left subtree, so preorder order is preserved: node, then everything in the left, then everything in the right. After the splice, `curr` has no left child and its `right` is the next preorder node, so we never need to look back at `curr`. The remaining unflattened part always sits to the right of `curr`.

## Where it goes wrong

The order of the writes. If you do `curr.right = curr.left` first, the original right subtree has no reference left and is lost. The splice `tail.right = curr.right` must come before it.

```text
Wrong:  curr.right = curr.left      (nothing points at 5 -> 6 any more)
        tail.right = curr.right     (curr.right is now the left subtree,
                                     so 4.right = 2: a loop, and 5, 6 are lost)
```

Forgetting `curr.left = None` leaves the left pointers behind and the result is not a list.

## Cost

Time O(n): the `tail` search can walk down the left subtree, but each node is walked over this way only once overall. Space O(1): just `curr` and `tail`.
