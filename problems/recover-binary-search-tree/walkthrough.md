## The idea

Read a valid BST left to right (inorder) and the values rise strictly. If two values were swapped, that sorted order is broken in a way you can spot: somewhere a value is smaller than the one before it. Find the two culprits from those drops, then swap their values back.

This needs no knowledge of the structure beyond the inorder walk, so it works however skewed the tree is.

## Set-up

- `stack` and `curr` run an iterative inorder walk: go as far left as possible pushing nodes, pop one to visit it, then move to its right child.
- `prev` is the node visited just before the current one.
- `first` and `second` are the two misplaced nodes, empty at first.

A drop is `prev.val > curr.val`. Two cases:

- The swapped values were not adjacent in the order: two drops. The first misplaced node is the larger one from the first drop, the second is the smaller one from the last drop.
- They were adjacent: only one drop, and both nodes come from it.

```text
tree:    3            inorder: 1, 3, 2, 4
        / \                       ^--^   one drop (3 then 2)
       1   4
          /
         2

first = second = prev = None
```

## Step by step

```text
visit 1   prev None            no check                 prev = 1
visit 3   prev 1,  1 > 3? no                            prev = 3
visit 2   prev 3,  3 > 2 yes   first = 3 (was None)
                               second = 2               prev = 2
visit 4   prev 2,  2 > 4? no                            prev = 4

first = 3, second = 2  ->  swap values: 3 <-> 2
```

The tree now reads inorder 1, 2, 3, 4. Two drops look like this:

```text
inorder: 5, 2, 3, 4, 1
         5>2 drop: first = 5, second = 2
         4>1 drop: first stays 5, second = 1
swap 5 and 1 -> 1, 2, 3, 4, 5
```

## Why it works

Swapping a big value `B` to an early spot and a small value `S` to a late spot makes `B` sit above its successor (a drop) and `S` sit below its predecessor (another drop). The big one is the earlier side of the first drop and the small one is the later side of the last drop. In the adjacent case the single drop contains both. Only values are swapped, so the tree shape and links stay as they are.

## Where it goes wrong

- Setting `first` on every drop. In the two-drop case `first` would end up at 4, the wrong node. It is assigned only when empty, while `second` is overwritten each time.
- Assuming there are always two drops. In the example above there is only one, and taking `second` only from a second drop would leave it empty.
- Checking children against the parent only (a local check) misses the problem: a bad value can be deep in the tree and still look fine next to its parent.

## Cost

Time O(n), each node is visited once. Space O(h) for the stack, where h is the tree height. (Morris traversal would make it O(1), but the stack version is simpler.)
