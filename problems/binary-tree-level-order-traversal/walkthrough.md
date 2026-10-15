## The idea

Level order means "all nodes at depth 0, then all at depth 1, and so on, left to right". A queue gives exactly that: nodes come out in the order they went in, so everything at one depth comes out before anything deeper.

The extra requirement is grouping nodes by level. The trick is to count. At the moment you start a level, the queue holds precisely that level's nodes, so `len(queue)` is the number of nodes to process before moving on.

## Set-up

- `queue` starts with just `root`. If `root` is `None`, return `[]` first; the queue would otherwise hold a `None` and `node.val` would crash.
- `result` is the list of levels.
- `level` is the list of values for the level being processed.
- The loop `for _ in range(len(queue))` evaluates `len(queue)` once, before any children are added. That frozen number is the level boundary.

## Step by step

Tree `[3,9,20,null,null,15,7]`:

```text
        3
       / \
      9   20
         /  \
        15   7
```

```text
Start       queue [3]                  result []

Level 1     size = 1
  pop 3     level [3]      push 9, 20
            queue [9, 20]              result [[3]]

Level 2     size = 2
  pop 9     level [9]      no children
  pop 20    level [9, 20]  push 15, 7
            queue [15, 7]              result [[3], [9, 20]]

Level 3     size = 2
  pop 15    level [15]
  pop 7     level [15, 7]
            queue []                   result [[3], [9, 20], [15, 7]]
```

The queue is empty, so the loop ends and `result` is `[[3], [9, 20], [15, 7]]`.

## Why it works

Children are added to the back of the queue, behind everything already there. So all nodes of depth `d` are ahead of all nodes of depth `d + 1`. When a level starts, the queue contains only that level, so frozen `len(queue)` pops exactly that level, and the children pushed meanwhile form the next one.

## Where it goes wrong

Writing `while queue` as the inner loop instead of `for _ in range(len(queue))`. The inner loop would never stop at a level boundary:

```text
inner loop on "while queue":  [3, 9, 20, 15, 7]   one big level
```

Reading `len(queue)` each time through (for example `while i < len(queue)`) has the same bug, because the length grows as children are pushed. Return `[]`, not `[[]]`, for an empty tree.

## Cost

Time O(n): each node enters and leaves the queue once. Space O(n): the queue can hold a whole level, up to about n/2 nodes, and the result holds all n values.
